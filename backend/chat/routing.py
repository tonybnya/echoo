from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chats/(?P<uri>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
