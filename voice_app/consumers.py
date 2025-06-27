import json
import asyncio
import websockets
import aiohttp
import base64
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

logger = logging.getLogger(__name__)

class RealTimeVoiceChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_ws = None
        self.openai_task = None

    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection established")
        
        # Connect to OpenAI Realtime API
        await self.connect_to_openai()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with code: {close_code}")
        
        # Clean up OpenAI connection
        if self.openai_task:
            self.openai_task.cancel()
        if self.openai_ws:
            await self.openai_ws.close()
        if hasattr(self, 'session') and self.session:
            await self.session.close()

    async def connect_to_openai(self):
        """Establish WebSocket connection to OpenAI Realtime API"""
        try:
            # Use aiohttp for better header support
            url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
            
            headers = {
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "OpenAI-Beta": "realtime=v1"
            }
            
            # Create aiohttp session
            self.session = aiohttp.ClientSession()
            self.openai_ws = await self.session.ws_connect(url, headers=headers)
            logger.info("Connected to OpenAI Realtime API")
            
            # Send session configuration
            await self.configure_session()
            
            # Start listening to OpenAI responses
            self.openai_task = asyncio.create_task(self.listen_to_openai())
            
        except Exception as e:
            logger.error(f"Failed to connect to OpenAI: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to connect to AI service'
            }))

    async def configure_session(self):
        """Configure the OpenAI Realtime session"""
        session_config = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": "You are a helpful and friendly AI assistant. Keep your responses conversational and natural. You can be interrupted at any time.",
                "voice": "alloy",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",  # Voice Activity Detection
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 500
                },
                "tool_choice": "auto",
                "temperature": 0.7
            }
        }
        
        await self.openai_ws.send_str(json.dumps(session_config))
        logger.info("Session configured")

    async def listen_to_openai(self):
        """Listen for responses from OpenAI Realtime API"""
        try:
            async for msg in self.openai_ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    await self.handle_openai_message(data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {self.openai_ws.exception()}")
                    break
        except Exception as e:
            logger.error(f"Error listening to OpenAI: {e}")

    async def handle_openai_message(self, data):
        """Handle different types of messages from OpenAI"""
        message_type = data.get('type')
        
        if message_type == 'response.audio.delta':
            # Stream audio data to client
            await self.send(text_data=json.dumps({
                'type': 'audio_delta',
                'audio': data.get('delta')  # Base64 encoded audio
            }))
            
        elif message_type == 'response.audio_transcript.delta':
            # Stream transcript of AI response
            await self.send(text_data=json.dumps({
                'type': 'ai_transcript_delta',
                'text': data.get('delta')
            }))
            
        elif message_type == 'conversation.item.input_audio_transcription.completed':
            # User's speech transcription
            await self.send(text_data=json.dumps({
                'type': 'user_transcript',
                'text': data.get('transcript')
            }))
            
        elif message_type == 'response.done':
            # Response completed
            await self.send(text_data=json.dumps({
                'type': 'response_done'
            }))
            
        elif message_type == 'input_audio_buffer.speech_started':
            # User started speaking
            await self.send(text_data=json.dumps({
                'type': 'user_speech_started'
            }))
            
        elif message_type == 'input_audio_buffer.speech_stopped':
            # User stopped speaking
            await self.send(text_data=json.dumps({
                'type': 'user_speech_stopped'
            }))
            
        elif message_type == 'error':
            logger.error(f"OpenAI error: {data}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': data.get('error', {}).get('message', 'Unknown error')
            }))

    async def receive(self, text_data):
        """Handle messages from the client"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'audio_data':
                # Forward audio data to OpenAI
                if self.openai_ws:
                    audio_message = {
                        "type": "input_audio_buffer.append",
                        "audio": data.get('audio')  # Base64 encoded audio
                    }
                    await self.openai_ws.send_str(json.dumps(audio_message))
                else:
                    logger.warning("OpenAI WebSocket not connected, skipping audio data")
                
            elif message_type == 'generate_response':
                # Trigger response generation
                if self.openai_ws:
                    response_message = {
                        "type": "response.create",
                        "response": {
                            "modalities": ["text", "audio"],
                            "instructions": "Please respond to the user's input."
                        }
                    }
                    await self.openai_ws.send_str(json.dumps(response_message))
                else:
                    logger.warning("OpenAI WebSocket not connected, cannot generate response")
                
            elif message_type == 'interrupt':
                # Interrupt current response
                if self.openai_ws:
                    interrupt_message = {
                        "type": "response.cancel"
                    }
                    await self.openai_ws.send_str(json.dumps(interrupt_message))
                else:
                    logger.warning("OpenAI WebSocket not connected, cannot interrupt")
                
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to process message'
            })) 