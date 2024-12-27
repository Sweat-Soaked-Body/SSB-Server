import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.exception import RoomException
from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # 데이터 수신
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': await self.get_username(),
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.save_message(
            room=await self.get_room(self.room_group_name),
            message=message
        )

        data = {
            'message': message,
            'user': await self.get_username(),
        }
        await self.send(text_data=json.dumps(data, ensure_ascii=False))

    @sync_to_async
    def get_room(self, room_group_name):
        room = Room.objects.filter(id=room_group_name).afirst()
        if room is None:
            raise RoomException.RoomNotFound
        return room

    @sync_to_async
    def save_message(self, room, message):
        Message.objects.acreate(
            room=room,
            service_user=self.scope['user'],
            message=message
        )

    @sync_to_async
    def get_username(self):
        return self.scope['user'].profile.name