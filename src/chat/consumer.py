import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.exception import RoomException
from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        user = self.scope["user"]

        await self.save_message(user, message, self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'message': message,
                'user': user,
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        data = {
            'message': message,
            'user': self.scope["user"],
        }
        await self.send(text_data=json.dumps(data, ensure_ascii=False))

    @sync_to_async
    def save_message(self, user, message, room_name):
        room = Room.objects.filter(id=room_name).first()
        if not room:
            raise RoomException.RoomNotFoundß

        Message.objects.create(
            room=room,
            user=user,
            text=message,
        )