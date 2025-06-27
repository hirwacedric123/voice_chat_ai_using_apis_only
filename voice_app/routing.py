from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/realtime-voice/', consumers.RealTimeVoiceChatConsumer.as_asgi()),
] 