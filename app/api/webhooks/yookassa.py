from api.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from var_dump import var_dump
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (
    WebhookNotificationEventType,
    WebhookNotificationFactory,
)


@api_view(['POST'])
def yookassaWebhookHandler(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # Если заголовок X-Forwarded-For отсутствует, получаем IP-адрес из REMOTE_ADDR.
        ip = request.META.get('REMOTE_ADDR')

    if not SecurityHelper().is_ip_trusted(ip):
        return Response({'error': 'Недопустимый отправитель'}, status=400)

    try:
        eventData = WebhookNotificationFactory().create(request.data)
        resp = eventData.object
        print('resp', var_dump(resp))
        if eventData.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED and resp.status == 'succeeded':
            if resp.metadata['product'] == 'inAppBalance':
                orderNumber = resp.metadata['orderNumber']
                order = Order.objects.filter(pk=orderNumber).first()
                if order:
                    order.status = 'alreadyPaid'
                    order.save()

        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)
