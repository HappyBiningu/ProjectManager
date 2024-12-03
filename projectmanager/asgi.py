import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Dynamically set settings module based on the environment
settings_module = 'projectmanager.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'projectmanager.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Add WebSocket routing here (to be added in future steps)
        ])
    ),
})
