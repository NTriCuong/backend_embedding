# backend_embedding/routing.py (hoặc project/routing.py)
from django.urls import path
from . import consumers  # hoặc đường dẫn đúng đến file consumer
#định nghĩa đường dẫn websocket
websocket_urlpatterns = [
    path("ws/handleface/", consumers.WebSocketConsumer.as_asgi()),
]
