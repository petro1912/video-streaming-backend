"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from app_auctions.background import BackgroundThread
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import app_auctions.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

asgi_application = get_asgi_application() #new
application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": URLRouter(app_auctions.routing.websocket_urlpatterns) 
})