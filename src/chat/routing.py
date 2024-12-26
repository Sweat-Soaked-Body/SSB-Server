from django.urls import path
from chat import consumer


websocket_urlpatterns = [
    path("ws/chat/<str:room_id>", consumer.ChatConsumer.as_asgi()),
]
