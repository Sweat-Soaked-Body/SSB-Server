from django.urls import path
from chat import consumer


urlpatterns = [
    path('/chat/<str:room_name>/', consumer.ChatConsumer.as_asgi()),
]
