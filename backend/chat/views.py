from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import ChatSession, ChatSessionMessage, ChatSessionParticipant, deserialize_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


class ChatSessionView(APIView):
    """Manage Chat sessions."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Create a new chat session."""
        user = request.user
        chat_session = ChatSession.objects.create(owner=user)

        return Response({
            'status': 'SUCCESS',
            'uri': chat_session.uri,
            'message': 'Chat session created successfully',
        }, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        """Add a user to a chat session."""
        User = get_user_model()
        uri = kwargs['uri']
        username = request.data.get('username')

        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        chat_session = get_object_or_404(ChatSession, uri=uri)
        owner = chat_session.owner

        if owner != user:
            chat_session.participants.get_or_create(
                user=user,
                chat_session=chat_session
            )

        owner_data = deserialize_user(owner)
        participants = [deserialize_user(part.user) for part in chat_session.participants.all()]

        participants.insert(0, owner_data)

        return Response({
            'status': 'SUCCESS',
            'participants': participants,
            'message': f'{user.username} joined the chat',
            'user': deserialize_user(user)
        })


class ChatSessionMessageView(APIView):
    """Create/Get Chat session messages."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Return all messages in a chat session."""
        uri = kwargs['uri']
        chat_session = get_object_or_404(ChatSession, uri=uri)
        messages = [chat_session_message.to_json() for chat_session_message in chat_session.messages.all()]

        return Response({
            'id': chat_session.id,
            'uri': chat_session.uri,
            'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """Create a new message in a chat session."""
        uri = kwargs['uri']
        message_text = request.data.get('message')

        if not message_text:
            return Response({'error': 'Message text is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        chat_session = get_object_or_404(ChatSession, uri=uri)
        ChatSessionMessage.objects.create(
            user=user,
            chat_session=chat_session,
            message=message_text
        )

        return Response({
            'status': 'SUCCESS',
            'uri': chat_session.uri,
            'message': deserialize_user(user)
        })