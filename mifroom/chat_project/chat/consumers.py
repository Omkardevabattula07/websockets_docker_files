import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json.get('message')
        file = text_data_json.get('file', None)
        image = text_data_json.get('image', None)
        user = self.scope['user']
        room = Room.objects.get(name=self.room_name)

        if content or file or image:
            message = Message.objects.create(user=user, room=room, content=content, file=file, image=image)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'user': user.username,
                        'content': content,
                        'file': message.file.url if message.file else None,
                        'image': message.image.url if message.image else None,
                    }
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
