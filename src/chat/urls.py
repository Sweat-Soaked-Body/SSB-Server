from django.urls import re_path
from chat import consumers


urlpatterns = [
    re_path(r'/chat/(?P<room_name>\w+)', consumers.ChatConsumer.as_asgi()),
]
