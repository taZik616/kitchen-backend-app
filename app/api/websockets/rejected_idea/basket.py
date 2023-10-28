import json

from api.models import BasketProduct, Customer
from api.serializers import BasketProductSerializer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.http import HttpRequest
from rest_framework.request import Request


def basketUpdate(customerId):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'basket_{customerId}', {
        'type': 'send.update', 'message': 'Корзина обновлена'})


class BasketConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            self.close()
            return
        self.customer = Customer.objects.filter(user=user).first()

        if not self.customer:
            self.close()
            return

        # self.userId = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'basket_{self.customer.id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'send.update'})

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        except:
            pass

    def send_update(self, event=None):
        basketQueryset = BasketProduct.objects.filter(
            customer=self.customer).order_by('id')
        httpRequest = HttpRequest()
        headersDict = {
            key.decode('utf-8'): value.decode('utf-8')
            for key, value in self.scope['headers']}
        httpRequest.META['HTTP_HOST'] = headersDict['host']
        request = Request(httpRequest)
        request.user = self.scope['user']

        serialized = BasketProductSerializer(
            basketQueryset, many=True, context={'request': request}).data

        self.send(text_data=json.dumps(serialized))
