

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.settings')

application = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from your_app_name.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator
from dashboard import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

