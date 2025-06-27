#!/usr/bin/env python
"""
Start the Voice Chat AI server with proper ASGI/WebSocket support
Usage: python start_server.py
"""
import os
import django
import uvicorn

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voice_chat_ai.settings')
django.setup()

if __name__ == "__main__":
    print("🎙️ Starting Voice Chat AI Server...")
    print("🌐 Server will be available at: http://127.0.0.1:8000")
    print("🎤 Real-time chat at: http://127.0.0.1:8000/realtime/")
    print("🔌 WebSocket support: ENABLED")
    print("\nPress CTRL+C to stop the server\n")
    
    # Start the server with import string for reload support
    uvicorn.run(
        "voice_chat_ai.asgi:application", 
        host="127.0.0.1", 
        port=8000, 
        log_level="info",
        reload=True  # Auto-reload on code changes
    )