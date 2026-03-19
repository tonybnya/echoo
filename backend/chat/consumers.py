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
        self.user = self.scope.get("user")

        logger.info(f"WebSocket connecting for URI: {self.uri}, user: {self.user}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        logger.info(f"WebSocket connected for URI: {self.uri}")

    async def disconnect(self, close_code):
        logger.info(
            f"WebSocket disconnected for URI: {self.uri} with code: {close_code}"
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            user_id = data.get("user_id")

            logger.info(
                f"Received message: '{message}' from user_id: {user_id} for URI: {self.uri}"
            )

            if not message:
                await self.send(text_data=json.dumps({"error": "Empty message"}))
                return

            saved_message = await self.save_message(user_id, self.uri, message)

            if saved_message:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat_message", "message": saved_message},
                )
            else:
                error_msg = "Failed to save message. Please rejoin the chat."
                logger.error(f"Failed to save message from user_id: {user_id}")
                await self.send(text_data=json.dumps({"error": error_msg}))

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send(text_data=json.dumps({"error": "Invalid message format"}))
        except Exception as e:
            logger.exception(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_message(self, user_id, uri, message_text):
        try:
            User = get_user()
            user = None

            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    logger.info(f"Found user by ID {user_id}: {user.username}")
                except User.DoesNotExist:
                    logger.warning(f"User with id {user_id} does not exist")
            elif hasattr(self, "user") and self.user and self.user.is_authenticated:
                user = self.user
                logger.info(f"Using authenticated user from scope: {user.username}")
            else:
                try:
                    user = User.objects.get(username="Guest")
                    logger.info("Falling back to Guest user")
                except User.DoesNotExist:
                    logger.error("No Guest user exists in database")
                    return None

            chat_session = ChatSession.objects.get(uri=uri)
            msg = ChatSessionMessage.objects.create(
                user=user, chat_session=chat_session, message=message_text
            )

            logger.info(f"Message saved: {msg.id} by {user.username}")

            participants = ChatSessionParticipant.objects.filter(
                chat_session=chat_session
            ).exclude(user=user)

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
                    channels=("console",),
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
