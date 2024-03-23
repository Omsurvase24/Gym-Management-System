"""
ASGI config for gymManageSys project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import main.routing
from channels.routing import ProtocolTypeRouter, URLRouter
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymManageSys.settings')


# application = get_asgi_application()
application = ProtocolTypeRouter({
    'websocket': URLRouter(main.routing.ws_patterns)
})
