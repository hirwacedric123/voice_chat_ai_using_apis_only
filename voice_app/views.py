from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import openai
import tempfile
import os
import logging
import traceback
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("Voice Chat AI Views Loaded")
if settings.OPENAI_API_KEY:
    logger.info(f"OpenAI API key configured (starts with: {settings.OPENAI_API_KEY[:7]}...)")
else:
    logger.error("OpenAI API key NOT configured - check your .env file")

def index(request):
    """Render the main voice chat interface."""
    return render(request, 'voice_app/index.html')

def realtime_index(request):
    """Render the real-time voice chat interface."""
    return render(request, 'voice_app/realtime.html')

@csrf_exempt
@require_http_methods(["POST"])
def voice_chat(request):
    """
    Main voice chat endpoint that processes audio through OpenAI APIs:
    1. Speech-to-Text (Whisper)
    2. ChatGPT processing
    3. Text-to-Speech
    """
    logger.info("=== Voice Chat Request Started ===")
    
    try:
        # Check if audio file is in the request
        if 'audio' not in request.FILES:
            logger.error("No audio file in request")
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio']
        logger.info(f"Received audio file: {audio_file.name}, size: {audio_file.size} bytes")
        
        # Validate file type
        if not audio_file.name.endswith(('.wav', '.mp3', '.m4a', '.webm')):
            logger.error(f"Unsupported audio format: {audio_file.name}")
            return JsonResponse({'error': 'Unsupported audio format'}, status=400)
        
        # Step 1: Speech-to-Text using OpenAI Whisper
        logger.info("Step 1: Starting speech-to-text transcription...")
        transcript = transcribe_audio(audio_file)
        if not transcript:
            logger.error("Speech-to-text transcription failed")
            return JsonResponse({'error': 'Failed to transcribe audio'}, status=500)
        logger.info(f"Transcription successful: '{transcript}'")
        
        # Step 2: Get AI response using ChatGPT
        logger.info("Step 2: Getting ChatGPT response...")
        ai_response = get_chatgpt_response(transcript)
        if not ai_response:
            logger.error("ChatGPT response generation failed")
            return JsonResponse({'error': 'Failed to get AI response'}, status=500)
        logger.info(f"ChatGPT response: '{ai_response}'")
        
        # Step 3: Convert AI response to speech
        logger.info("Step 3: Converting text to speech...")
        audio_response = text_to_speech(ai_response)
        if not audio_response:
            logger.error("Text-to-speech conversion failed")
            return JsonResponse({'error': 'Failed to generate speech'}, status=500)
        logger.info(f"TTS successful, audio size: {len(audio_response)} bytes")
        
        # Return the audio file as response
        response = HttpResponse(audio_response, content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="ai_response.mp3"'
        
        # Also include the text in headers for debugging
        response['X-Transcript'] = transcript
        response['X-AI-Response'] = ai_response
        
        logger.info("=== Voice Chat Request Completed Successfully ===")
        return response
        
    except Exception as e:
        logger.error(f"Voice chat error: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)

def transcribe_audio(audio_file):
    """Convert audio to text using OpenAI Whisper API."""
    temp_file_path = None
    try:
        logger.info("Creating temporary file for audio transcription...")
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        logger.info(f"Temporary file created: {temp_file_path}")
        
        # Check if API key is available
        if not settings.OPENAI_API_KEY:
            logger.error("OpenAI API key not configured")
            return None
        
        # Transcribe using OpenAI Whisper
        logger.info("Sending audio to OpenAI Whisper API...")
        logger.info(f"Using API key (first 7 chars): {settings.OPENAI_API_KEY[:7]}...")
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        with open(temp_file_path, 'rb') as audio_data:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_data,
                response_format="text"
            )
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        logger.info("Temporary file cleaned up")
        
        result = transcript.strip()
        logger.info(f"Transcription completed successfully, length: {len(result)} characters")
        return result
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        logger.error(f"Transcription traceback: {traceback.format_exc()}")
        # Clean up on error
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info("Cleaned up temporary file after error")
            except Exception as cleanup_error:
                logger.error(f"Failed to cleanup temp file: {cleanup_error}")
        return None

def get_chatgpt_response(text):
    """Get AI response using ChatGPT API."""
    try:
        logger.info(f"Sending message to ChatGPT: '{text}' (length: {len(text)} chars)")
        
        # Check if API key is available
        if not settings.OPENAI_API_KEY:
            logger.error("OpenAI API key not configured")
            return None
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        logger.info("Calling OpenAI ChatGPT API...")
        logger.info(f"Using API key (first 7 chars): {settings.OPENAI_API_KEY[:7]}...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful and friendly AI assistant. Keep your responses conversational and natural, as they will be converted to speech. Avoid using special characters or formatting that don't translate well to speech."
                },
                {"role": "user", "content": text}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        result = response.choices[0].message.content.strip()
        logger.info(f"ChatGPT response received, length: {len(result)} characters")
        logger.info(f"Tokens used - Prompt: {response.usage.prompt_tokens}, Completion: {response.usage.completion_tokens}")
        return result
        
    except Exception as e:
        logger.error(f"ChatGPT error: {str(e)}")
        logger.error(f"ChatGPT traceback: {traceback.format_exc()}")
        return None

def text_to_speech(text):
    """Convert text to speech using OpenAI TTS API."""
    try:
        logger.info(f"Converting text to speech: '{text}' (length: {len(text)} chars)")
        
        # Check if API key is available
        if not settings.OPENAI_API_KEY:
            logger.error("OpenAI API key not configured")
            return None
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        logger.info("Calling OpenAI TTS API...")
        logger.info(f"Using API key (first 7 chars): {settings.OPENAI_API_KEY[:7]}...")
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # You can change this to: alloy, echo, fable, onyx, nova, shimmer
            input=text,
            response_format="mp3"
        )
        
        audio_content = response.content
        logger.info(f"TTS completed successfully, audio size: {len(audio_content)} bytes")
        return audio_content
        
    except Exception as e:
        logger.error(f"Text-to-speech error: {str(e)}")
        logger.error(f"TTS traceback: {traceback.format_exc()}")
        return None

@csrf_exempt
@require_http_methods(["POST"])
def test_transcript_only(request):
    """Test endpoint that only returns the transcript (for debugging)."""
    try:
        if 'audio' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio']
        transcript = transcribe_audio(audio_file)
        
        return JsonResponse({
            'transcript': transcript,
            'success': True
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
