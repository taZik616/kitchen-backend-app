from api.decorators import onlyCustomer
from api.models import SupportRequest
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
    SupportRequest.objects.create(message=message, customer=customer)

    return Response({'success': 'Запрос отправлен'})
