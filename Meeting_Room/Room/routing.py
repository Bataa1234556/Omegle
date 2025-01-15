# your_app_name/routing.py
from django.urls import re_path
from .consumers import OmegleConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', OmegleConsumer.as_asgi()),  # No room name, pairing handled automatically
]
