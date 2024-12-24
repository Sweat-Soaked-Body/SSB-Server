from django.urls import re_path

from chat import consumer


urlpatterns = [
    re_path(r'/ws/chat/(?P<room_name>\w+)', consumer.ChatConsumer.as_asgi()),
]
