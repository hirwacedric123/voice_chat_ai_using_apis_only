from django.urls import path
from . import views

app_name = 'voice_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('voice-chat/', views.voice_chat, name='voice_chat'),
    path('test-transcript/', views.test_transcript_only, name='test_transcript'),
] 