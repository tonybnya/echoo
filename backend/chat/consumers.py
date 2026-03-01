import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatSession, ChatSessionMessage, deserialize_user

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.uri = self.scope['url_route']['kwargs']['uri']
        self.room_group_name = f'chat_{self.uri}'

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
        message = data.get('message')
        user_id = data.get('user_id') # We'll send this from frontend for now, or use scope['user'] if authenticated

        if not message:
            return

        # Save message to database
        saved_message = await self.save_message(user_id, self.uri, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved_message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, user_id, uri, message_text):
        user = User.objects.get(id=user_id)
        chat_session = ChatSession.objects.get(uri=uri)
        msg = ChatSessionMessage.objects.create(
            user=user,
            chat_session=chat_session,
            message=message_text
        )
        return msg.to_json()
