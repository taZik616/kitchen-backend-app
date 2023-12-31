from api.decorators import onlyCustomer
from api.models import Order, SupportRequest
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view
from rest_framework.response import Response


@ratelimit(key='user_or_ip', rate='5/d', block=False)
@api_view(['POST'])
@onlyCustomer
def makeSupportRequestView(request, customer):
    is_blocked = getattr(request, 'limited', False)
    if is_blocked:
        return Response({'error': 'Вы превысили лимит запросов, повторите завтра'}, status=400)

    message = request.data.get('message')
    orderId = request.data.get('orderId')

    order = None
    if orderId:
        order = Order.objects.filter(pk=orderId).first()

    SupportRequest.objects.create(
        message=message, customer=customer, order=order)

    return Response({'success': 'Запрос отправлен'})
