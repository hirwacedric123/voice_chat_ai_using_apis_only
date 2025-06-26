# 🎙️ AI Voice Chat Application

A comprehensive Django-based voice chat application that creates natural conversations with AI using OpenAI's state-of-the-art APIs. This implementation uses a simple HTTP-based architecture for reliable voice processing.

## 🌟 Features

- **🎤 Speech-to-Text**: High-quality voice transcription using OpenAI Whisper
- **🤖 AI Conversation**: Intelligent responses powered by ChatGPT
- **🔊 Text-to-Speech**: Natural voice synthesis with OpenAI TTS
- **🌐 Modern Web Interface**: Beautiful, responsive UI with real-time feedback
- **📊 Comprehensive Logging**: Detailed debugging and monitoring capabilities
- **🔧 Easy Configuration**: Simple setup with environment variables
- **🛡️ Error Handling**: Robust error handling and user feedback

## 🏗️ Architecture & Workflow

### 📋 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser       │    │   Django        │    │   OpenAI        │
│   Frontend      │    │   Backend       │    │   APIs          │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Audio Capture │    │ • Request       │    │ • Whisper       │
│ • MediaRecorder │◄──►│   Handling      │◄──►│ • GPT-3.5-turbo │
│ • Audio Player  │    │ • File          │    │ • TTS-1         │
│ • UI Updates    │    │   Management    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔄 Complete Workflow

#### **Phase 1: Audio Capture**
1. **User clicks microphone** → Browser requests microphone access
2. **Recording starts** → MediaRecorder captures audio in WebM format
3. **User clicks stop** → Audio recording ends, creates Blob

#### **Phase 2: Backend Processing**
4. **Audio upload** → FormData with audio file sent via HTTP POST
5. **File validation** → Django validates file type and size
6. **Temporary storage** → Audio saved to temporary file

#### **Phase 3: OpenAI API Chain**
7. **Speech-to-Text** → Whisper API converts audio to text
8. **AI Processing** → ChatGPT generates conversational response
9. **Text-to-Speech** → TTS API converts response to MP3 audio

#### **Phase 4: Response Delivery**
10. **Audio streaming** → MP3 file streamed back to browser
11. **UI updates** → Transcript and response text displayed
12. **Audio playback** → Browser plays AI's voice response

## 🤖 OpenAI Models Used

### 🎯 **Whisper (Speech-to-Text)**
- **Model**: `whisper-1`
- **Capabilities**: Multilingual speech recognition
- **Accuracy**: Industry-leading transcription quality
- **Input**: Audio files (WebM, MP3, WAV, M4A)
- **Output**: Plain text transcription
- **Cost**: $0.006 per minute

### 🧠 **ChatGPT (Conversation)**
- **Model**: `gpt-3.5-turbo`
- **Capabilities**: Natural conversation, context understanding
- **Configuration**: 
  - Max tokens: 150 (optimized for speech)
  - Temperature: 0.7 (balanced creativity)
  - System prompt: Conversational and speech-friendly
- **Cost**: $0.0015 per 1K input tokens, $0.002 per 1K output tokens

### 🗣️ **Text-to-Speech (Voice Synthesis)**
- **Model**: `tts-1`
- **Voice**: `alloy` (customizable)
- **Available voices**: alloy, echo, fable, onyx, nova, shimmer
- **Output format**: MP3
- **Quality**: Natural, human-like speech
- **Cost**: $0.015 per 1K characters

## 🚀 Quick Start

### 1. **Clone & Setup**
```bash
git clone <your-repo>
cd voice_chat_ai
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure OpenAI API**
```bash
# Run the setup script
python setup_env.py

# Or manually create .env file:
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 4. **Initialize Database**
```bash
python manage.py migrate
```

### 5. **Test Configuration**
```bash
python manage.py test_api_key
```

### 6. **Start Server**
```bash
python manage.py runserver
```

### 7. **Open Application**
Navigate to `http://127.0.0.1:8000/`

## 🛠️ Configuration Options

### 🎵 **Voice Customization**
```python
# In voice_app/views.py - text_to_speech function
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
    input=text,
    response_format="mp3"
)
```

### 🤖 **AI Personality**
```python
# In voice_app/views.py - get_chatgpt_response function
{
    "role": "system", 
    "content": """You are a helpful and friendly AI assistant. 
                 Keep responses conversational and natural for speech.
                 Avoid special characters and complex formatting."""
}
```

### ⚙️ **Performance Tuning**
```python
# In voice_chat_ai/settings.py
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# ChatGPT response optimization
max_tokens=150,      # Shorter responses for faster processing
temperature=0.7,     # Balanced creativity vs speed
```

## 📋 API Endpoints

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/` | GET | Main voice chat interface | HTML page |
| `/voice-chat/` | POST | Process voice → AI response | MP3 audio + headers |
| `/test-transcript/` | POST | Test transcription only | JSON with transcript |

### 📤 **Request Format** (`/voice-chat/`)
```javascript
FormData {
    audio: Blob (WebM audio file)
}
```

### 📥 **Response Format**
```http
Content-Type: audio/mpeg
Content-Disposition: attachment; filename="ai_response.mp3"
X-Transcript: "User's spoken text"
X-AI-Response: "AI's text response"

[MP3 audio data]
```

## 📊 Performance Characteristics

### ⏱️ **Typical Response Times**
- **Audio Recording**: 0-5 seconds (user controlled)
- **File Upload**: 100-500ms (depends on audio size)
- **Whisper Transcription**: 2-5 seconds
- **ChatGPT Response**: 1-3 seconds
- **TTS Generation**: 2-4 seconds
- **Total Processing**: 5-12 seconds

### 📈 **Factors Affecting Speed**
- Audio file size (longer recordings = slower upload)
- Network latency to OpenAI servers
- OpenAI API response times (varies by load)
- Audio quality and complexity

### 🎯 **Optimization Opportunities**
1. **Parallel Processing**: Run multiple API calls simultaneously
2. **Streaming**: Use streaming APIs for real-time responses
3. **Caching**: Cache common responses
4. **Audio Compression**: Optimize audio encoding
5. **WebRTC**: Real-time audio streaming

## 🔧 Troubleshooting

### 🎤 **Microphone Issues**
```bash
# Check browser permissions
# Ensure HTTPS in production
# Test with different browsers
```

### 🔑 **API Key Problems**
```bash
# Test API key
python manage.py test_api_key

# Check .env file
cat .env

# Verify OpenAI account credits
```

### 🐛 **Audio Processing Errors**
```bash
# Check server logs for detailed errors
# Verify supported audio formats
# Test with shorter audio clips
```

### 📊 **Performance Issues**
```bash
# Monitor network requests in browser dev tools
# Check OpenAI API status
# Optimize audio file size
```

## 📁 Project Structure

```
voice_chat_ai/
├── 📁 voice_app/                    # Main Django application
│   ├── 📁 management/               # Custom Django commands
│   │   └── 📁 commands/
│   │       └── 📄 test_api_key.py   # API key testing utility
│   ├── 📁 templates/voice_app/      # HTML templates
│   │   └── 📄 index.html            # Main voice chat interface
│   ├── 📄 views.py                  # Core voice processing logic
│   ├── 📄 urls.py                   # URL routing
│   └── 📄 models.py                 # Database models (if needed)
├── 📁 voice_chat_ai/                # Django project configuration
│   ├── 📄 settings.py               # Project settings
│   ├── 📄 urls.py                   # Root URL configuration
│   └── 📄 wsgi.py                   # WSGI configuration
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env                          # Environment variables (create this)
├── 📄 .gitignore                    # Git ignore rules
├── 📄 setup_env.py                  # Environment setup script
├── 📄 debug_api_key.py              # API key debugging utility
└── 📄 README.md                     # This documentation
```

## 🔐 Security & Best Practices

### 🛡️ **Environment Security**
- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly
- Monitor API usage and costs

### 🌐 **Web Security**
- Use HTTPS in production for microphone access
- Validate all file uploads
- Implement rate limiting for API calls
- Sanitize user inputs

### 📊 **Monitoring**
- Log all API calls and responses
- Monitor error rates and performance
- Set up alerts for API failures
- Track usage costs

## 💰 Cost Analysis

### 📊 **Usage-Based Pricing**

| Component | Cost | Typical Usage | Example Cost |
|-----------|------|---------------|--------------|
| Whisper STT | $0.006/minute | 10 conversations/day (5 min each) | $0.30/day |
| ChatGPT | $0.0015-0.002/1K tokens | 150 tokens avg/response | $0.03/day |
| TTS | $0.015/1K chars | 100 chars avg/response | $0.15/day |
| **Total** | | **Daily development usage** | **~$0.50/day** |

### 💡 **Cost Optimization Tips**
- Use shorter audio recordings
- Optimize ChatGPT token usage
- Implement response caching
- Monitor and set usage limits

## 🚀 Future Improvements

### 🔥 **Performance Enhancements**
1. **Real-time Streaming**: WebSocket implementation
2. **Parallel API Calls**: Simultaneous processing
3. **Audio Compression**: Reduce file sizes
4. **Edge Caching**: Faster response times

### 🎯 **Feature Additions**
1. **Conversation Memory**: Multi-turn conversations
2. **Voice Selection**: Multiple TTS voices
3. **Language Support**: Multilingual conversations
4. **Conversation History**: Save and replay chats

### 🛠️ **Technical Upgrades**
1. **WebRTC Integration**: Real-time audio streaming
2. **Progressive Web App**: Offline capabilities
3. **Mobile Optimization**: Touch-friendly interface
4. **API Rate Limiting**: Better error handling

## 🤝 Contributing

### 🐛 **Bug Reports**
- Use the issue tracker
- Include detailed logs
- Provide reproduction steps

### 💡 **Feature Requests**
- Describe the use case
- Consider performance implications
- Provide implementation suggestions

### 🔧 **Pull Requests**
- Follow existing code style
- Add tests for new features
- Update documentation

## 📄 License

This project is open source and available under the MIT License.

---

## 🎉 Quick Test Checklist

- [ ] ✅ Dependencies installed (`pip install -r requirements.txt`)
- [ ] ✅ OpenAI API key configured (`.env` file)
- [ ] ✅ API key tested (`python manage.py test_api_key`)
- [ ] ✅ Server running (`python manage.py runserver`)
- [ ] ✅ Browser microphone access granted
- [ ] ✅ Voice recording working
- [ ] ✅ AI responses generating
- [ ] ✅ Audio playback functioning

**Happy voice chatting with AI! 🎙️🤖**
