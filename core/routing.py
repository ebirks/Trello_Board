from django.urls import re_path
from .consumers import BoardConsumer

websocket_urlpatterns = [
    # This URL will be: ws://127.0.0.1:8000/ws/board/3/
    re_path(r'ws/board/(?P<board_id>\d+)/$', BoardConsumer.as_asgi()),
]