from api.constants import TIME_HOUR
from api.models import Customer
from api.utils import ActionLimiter, sendCodeToPhone, validateAndFormatPhoneNumber
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response


@ratelimit(key='ip', rate='15/5min', block=False)
@api_view(['POST'])
def loginView(request):
    """Для того чтобы получить токен нужны поля `username` и `password`"""
    is_blocked = getattr(request, 'limited', False)
    if is_blocked:
        return Response({'error': 'Вы превысили лимит запросов, повторите через минуту'}, status=400)

    username = request.data.get('username')

    res = validateAndFormatPhoneNumber(username)
    if not res.get('success'):
        return Response({"error": res['error']}, status=400)

    try:
        username = res['formattedPhoneNumber']
        formattedPhoneNumber = res['formattedPhoneNumberInternational']

        customer = Customer.objects.filter(user__username=username).first()
        if not customer:
            return Response({'error': 'Пользователь с таким номером не найден'}, status=400)
        if not customer.user.is_active:
            return Response({'error': 'Пользователь был удален'}, status=400)

        # Code send
        codeSendRes = sendCodeToPhone(username)
        code = codeSendRes.get('code')
        print('🚀 - code:', code)

        if not code:
            return Response(codeSendRes, status=400)
        # ---------
        cacheKey = f'login-code-{username[1:]}'

        cache.set(cacheKey, {
            **cache.get(cacheKey, {}),
            'code': code,
        }, TIME_HOUR)

        return Response({
            'formattedPhoneNumber': formattedPhoneNumber,
            'details': 'У вас есть час чтобы использовать код',
            'success': True
        })
    except:
        return Response({"error": 'Не удалось разрешить доступ'}, status=400)


loginConfirmLimiter = ActionLimiter('login-confirm-', 30, TIME_HOUR, TIME_HOUR)


@api_view(['POST'])
def loginConfirmView(request):
    addressIP = request.META.get('REMOTE_ADDR')
    username = request.data.get('username')
    supposedCode = request.data.get('supposedCode')

    if loginConfirmLimiter.getIsBlocked(addressIP):
        return Response(
            {'error': 'Вы превысили лимит, повторите через час'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    res = validateAndFormatPhoneNumber(username)
    if not res.get('success'):
        return Response({"error": res['error']}, status=400)

    username = res['formattedPhoneNumber']
    customer = Customer.objects.filter(user__username=username).first()
    if not customer:
        return Response({'error': 'Пользователь с таким номером не найден'}, status=400)
    try:
        cacheKey = f'login-code-{username[1:]}'
        cacheObj = cache.get(cacheKey, {})
        code = cacheObj.pop('code', '')

        if str(code) != str(supposedCode):
            loginConfirmLimiter.increment(addressIP)
            return Response({'error': 'Код не подходит'}, status=400)

        tokenTuple = Token.objects.get_or_create(user=customer.user)

        return Response({
            'success': 'Вы успешно вошли',
            'token': tokenTuple[0].key})

    except:
        return Response({"error": 'Не удалось разрешить доступ'}, status=400)
