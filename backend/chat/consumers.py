import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from notifications.utils import notify
from .models import (
    ChatSession,
    ChatSessionMessage,
    ChatSessionParticipant,
    deserialize_user,
)

logger = logging.getLogger(__name__)


def get_user():
    return get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.uri = self.scope["url_route"]["kwargs"]["uri"]
        self.room_group_name = f"chat_{self.uri}"

        logger.info(f"WebSocket connecting for URI: {self.uri}")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        logger.info(f"WebSocket connected for URI: {self.uri}")

    async def disconnect(self, close_code):
        logger.info(
            f"WebSocket disconnected for URI: {self.uri} with code: {close_code}"
        )
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            user_id = data.get("user_id")

            logger.info(
                f"Received message: {message} from user_id: {user_id} for URI: {self.uri}"
            )

            if not message:
                return

            # Save message to database
            saved_message = await self.save_message(user_id, self.uri, message)

            if saved_message:
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat_message", "message": saved_message},
                )
            else:
                logger.error(f"Failed to save message from user_id: {user_id}")
                # Optionally send an error message back to the sender
                await self.send(
                    text_data=json.dumps(
                        {"error": "Message could not be saved. Are you logged in?"}
                    )
                )

        except Exception as e:
            logger.exception(f"Error in receive: {e}")

    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_message(self, user_id, uri, message_text):
        try:
            # Fallback to Guest user (ID 7) if no user_id is provided
            if not user_id:
                logger.info(
                    f"No user_id provided for URI {uri}, falling back to Guest (ID 7)"
                )
                user_id = 7

            user = get_user().objects.get(id=user_id)
            chat_session = ChatSession.objects.get(uri=uri)
            msg = ChatSessionMessage.objects.create(
                user=user, chat_session=chat_session, message=message_text
            )

            # Trigger notification for other participants
            participants = ChatSessionParticipant.objects.filter(
                chat_session=chat_session
            ).exclude(user=user)
            # Also include the owner if they are not the sender
            if chat_session.owner != user:
                # We need to be careful with duplicates if the owner is also a participant record
                # But usually participants includes everyone. Let's check models.
                pass

            # Simplified: Notify all participants except sender
            # In our current models, owner is separate from participants list?
            # Let's check: ChatSession.owner and ChatSessionParticipant
            recipients = [p.user for p in participants]
            if chat_session.owner != user and chat_session.owner not in recipients:
                recipients.append(chat_session.owner)

            for recipient in recipients:
                notify(
                    recipient=recipient,
                    source=user,
                    action="sent a message",
                    short_description=message_text[:50],
                    url=f"/chats/{uri}",
                    channels=("rabbitmq", "console"),
                )

            return msg.to_json()
        except get_user().DoesNotExist:
            logger.error(f"User with id {user_id} does not exist")
            return None
        except ChatSession.DoesNotExist:
            logger.error(f"Chat session with URI {uri} does not exist")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error saving message: {e}")
            return None
