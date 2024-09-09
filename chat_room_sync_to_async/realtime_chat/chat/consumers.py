# chat/consumers.py
import base64
import json
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room

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
        data = json.loads(text_data)
        message_type = data.get('type', 'text')

        # Handling different types of messages
        if message_type == 'text':
            message = data['message']
            await self.save_message(self.room_name, message)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'message_type': 'text',
                }
            )
        elif message_type in ['image', 'audio', 'video']:
            file_data = data['file']
            file_format, file_str = file_data.split(';base64,')
            ext = file_format.split('/')[-1]
            file_content = ContentFile(base64.b64decode(file_str), name=f"{message_type}.{ext}")

            # Save message to database
            message_obj = await self.save_file_message(self.room_name, file_content, message_type)
            
            # Send file to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'file_url': message_obj.file.url,
                    'message_type': message_type,
                }
            )

    async def chat_message(self, event):
        message_type = event['message_type']

        # Sending the message back to the client based on the type
        if message_type == 'text':
            message = event['message']
            await self.send(text_data=json.dumps({
                'type': 'text',
                'message': message
            }))
        elif message_type in ['image', 'audio', 'video']:
            file_url = event['file_url']
            await self.send(text_data=json.dumps({
                'type': message_type,
                'file_url': file_url
            }))

    @sync_to_async
    def save_message(self, room_name, message):
        room = Room.objects.get(name=room_name)
        Message.objects.create(room=room, content=message, message_type='text')

    @sync_to_async
    def save_file_message(self, room_name, file, message_type):
        room = Room.objects.get(name=room_name)
        return Message.objects.create(room=room, file=file, message_type=message_type)
