from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.urls import re_path
from rest_framework.authtoken.models import Token

websocket_urlpatterns = [
    # re_path(r'ws/v1/basket', basket.BasketConsumer.as_asgi()),
]


@database_sync_to_async
def getUser(tokenKey):
    token = Token.objects.filter(key=tokenKey).first()
    if token:
        return token.user
    else:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        scope['user'] = AnonymousUser()

        if b'authorization' in headers:
            auth = headers[b'authorization']
            tokenName, tokenKey = auth.decode().split()

            if tokenName == 'Token':
                scope['user'] = await getUser(tokenKey)

        return await self.app(scope, receive, send)
