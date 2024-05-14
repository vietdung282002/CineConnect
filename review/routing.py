from django.urls import path
from .consumers import ReactionConsumer

websocket_urlpatterns = [
    path('ws/reactions/', ReactionConsumer.as_asgi()),
    # ws://127.0.0.1:8000/ws/reactions/
]