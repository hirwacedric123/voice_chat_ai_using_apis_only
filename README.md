# 🎙️ AI Voice Chat Application

A simple Django-based voice chat application that uses OpenAI APIs for Speech-to-Text, ChatGPT, and Text-to-Speech functionality.

## 🌟 Features

- **HTTP-based**: No WebSockets needed - simple request/response pattern
- **Speech-to-Text**: Convert your voice to text using OpenAI Whisper
- **AI Conversation**: Get intelligent responses from ChatGPT
- **Text-to-Speech**: Hear AI responses with natural voice synthesis
- **Modern UI**: Beautiful, responsive interface with real-time feedback

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up OpenAI API Key

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start the Development Server

```bash
python manage.py runserver
```

### 5. Open Your Browser

Navigate to `http://127.0.0.1:8000/` and start chatting with AI using your voice!

## 🎯 How It Works

1. **User speaks** → Browser captures audio
2. **Audio upload** → Django receives audio file via HTTP POST
3. **Speech-to-Text** → OpenAI Whisper converts audio to text
4. **AI Processing** → ChatGPT generates intelligent response
5. **Text-to-Speech** → OpenAI TTS converts response to audio
6. **Audio playback** → Browser plays AI response

## 📋 API Endpoints

- `GET /` - Main voice chat interface
- `POST /voice-chat/` - Process voice input and return audio response
- `POST /test-transcript/` - Test endpoint for transcription only

## 🛠️ Configuration

### Available TTS Voices

You can change the AI voice in `voice_app/views.py`:

```python
# Available voices: alloy, echo, fable, onyx, nova, shimmer
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",  # Change this
    input=text,
    response_format="mp3"
)
```

### Customize AI Personality

Modify the system prompt in `voice_app/views.py`:

```python
{
    "role": "system", 
    "content": "Your custom AI personality here..."
}
```

## 📱 Browser Requirements

- **Microphone access required**
- **HTTPS recommended** for production (HTTP works for localhost)
- **Modern browser** with MediaRecorder API support

## 🔧 Troubleshooting

### Microphone Access Denied

- Allow microphone permissions in your browser
- Use HTTPS in production environments

### OpenAI API Errors

- Verify your API key is correct
- Check your OpenAI account has sufficient credits
- Ensure API key has the required permissions

### Audio Format Issues

- Supported formats: WAV, MP3, M4A, WebM
- Browser will typically use WebM for recording

## 📁 Project Structure

```
voice_chat_ai/
├── voice_app/              # Main Django app
│   ├── templates/         # HTML templates
│   ├── views.py          # Voice chat logic
│   └── urls.py           # URL routing
├── voice_chat_ai/        # Django project settings
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## 🔐 Security Notes

- Keep your `.env` file secure and never commit it to version control
- The `.env` file is in `.gitignore` by default
- In production, use environment variables or secure secret management

## 🎨 Customization

The application is designed to be easily customizable:

- **UI**: Modify `voice_app/templates/voice_app/index.html`
- **AI Logic**: Update `voice_app/views.py`
- **Styling**: Edit the CSS in the template
- **Voice Settings**: Change TTS voice and ChatGPT parameters

## 📊 Costs

This application uses OpenAI APIs which have usage-based pricing:

- **Whisper (STT)**: $0.006 per minute
- **ChatGPT**: Varies by model (GPT-3.5-turbo recommended for cost)
- **TTS**: $0.015 per 1K characters

For development and testing, costs are typically very low.

## 🤝 Contributing

Feel free to submit issues and pull requests to improve this voice chat application!

## 📄 License

This project is open source and available under the MIT License.
