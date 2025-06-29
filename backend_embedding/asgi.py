# asgi.py
import os
import django 
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from api_real_time.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_embedding.settings')

django.setup()  
application = ProtocolTypeRouter({
    "websocket":(
        URLRouter(websocket_urlpatterns)
    ),
})
