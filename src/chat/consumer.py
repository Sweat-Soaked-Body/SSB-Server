import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.exception import RoomException
from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # room name 파싱
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.channel_name = self.room_id

        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_id,
            self.channel_name
        )

    # 데이터 수신
    async def receive(self, text_data):
        message = json.loads(text_data)

        room = await self.get_room(self.room_id)

        await self.save_message(
            room=room,
            message=message['message']
        )

        username = await self.get_username()

        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'chat_message',
                'user': username,
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = await self.get_username()
        data = {
            'message': message,
            'user': username,
        }
        await self.send(text_data=json.dumps(data, ensure_ascii=False))

    @sync_to_async
    def get_room(self, room_id):
        room = Room.objects.filter(id=room_id).afirst()
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