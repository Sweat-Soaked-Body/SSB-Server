import json
from datetime import datetime

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

        message = await self.get_past_messages()
        await self.send(text_data=json.dumps(message, ensure_ascii=False, default=str))

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
        await self.send(text_data=json.dumps(data, ensure_ascii=False, default=str))

    @sync_to_async
    def get_room(self, room_group_name):
        room = Room.objects.filter(id=room_group_name).first()
        if room is None:
            raise RoomException.RoomNotFound
        return room

    @sync_to_async
    def save_message(self, room, message):
        Message.objects.create(
            room=room,
            service_user=self.scope['user'],
            message=message
        )

    @sync_to_async
    def get_username(self):
        return self.scope['user'].profile.name

    @sync_to_async
    def get_messages_for_room(self, room):
        return list(Message.objects.filter(room=room).select_related("service_user__profile"))

    async def get_past_messages(self):
        room = await self.get_room(self.room_group_name)

        messages = await self.get_messages_for_room(room)

        return [
            {
                'message': message.message,
                'user': message.service_user.profile.name,
                'timestamp': message.timestamp,
            }
            for message in messages
        ]