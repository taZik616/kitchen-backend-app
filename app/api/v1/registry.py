from api.constants import TIME_DAY, TIME_HOUR
from api.models import BaseUser, City, Customer
from api.utils import (
    ActionLimiter,
    generatePassword,
    sendCodeToPhone,
    validateAndFormatPhoneNumber,
)
from django.core.cache import cache
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

registryLimiter = ActionLimiter('registry-', 6, TIME_HOUR, TIME_HOUR)
registryConfirmLimiter = ActionLimiter(
    'registry-confirm-', 30, TIME_HOUR, TIME_HOUR)
resendLimiter = ActionLimiter('registry-resend-code-', 1, 60*5, 60*5)


@api_view(['POST'])
def registrySendCodeView(request):
    # Get data
    addressIP = request.META.get('REMOTE_ADDR')

    username = request.data.get('username')
    name = request.data.get('name', '')
    city = request.data.get('cityId')

    isBlocked = registryLimiter.getIsBlocked(addressIP)
    # ---------

    # Validation
    if isBlocked:
        return Response({'error': 'Вы превысили лимит запросов, повторите через час'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    if not username:
        return Response({'error': 'Укажите номер телефона'}, status=400)

    res = validateAndFormatPhoneNumber(username)
    if not res['success']:
        return Response({'error': res.get('error')}, status=400)

    if not city:
        return Response({'error': 'Для регистрации нужно выбрать ваш город из списка доступных'}, status=400)
    city = City.objects.filter(id=city).first()
    if not city:
        return Response({'error': 'Населенный пункт с данным идентификатором не найден'}, status=400)

    username = res['formattedPhoneNumber']

    isUserAlreadyExist = BaseUser.objects.filter(username=username).exists()
    if isUserAlreadyExist:
        return Response({'error': 'Аккаунт с данным номером уже был создан'}, status=400)
    # ---------

    # Send code
    codeSendRes = sendCodeToPhone(username)
    code = codeSendRes.get('code')
    print('🚀 - code:', code)
    if not code:
        return Response(codeSendRes, status=400)
    # ---------

    # Create user, set expiration and increment limiter
    cacheKey = f'registration-code-{username[1:]}'
    cache.set(cacheKey, {
        **cache.get(cacheKey, {}),
        'code': code
    }, TIME_DAY)
    baseUser = BaseUser.objects.create_user(
        username=username,
        password=generatePassword(),
    )
    Customer.objects.create(
        user=baseUser,
        name=name,
        city=city
    )

    registryLimiter.increment(addressIP)
    # ---------

    return Response({
        'success': 'На номер был отправлен звонок с кодом',
        'formattedPhoneNumber': res.get('formattedPhoneNumberInternational')
    })


@api_view(['POST'])
def registryResendCodeView(request):
    # Get data
    addressIP = request.META.get('REMOTE_ADDR')
    isBlocked = resendLimiter.getIsBlocked(addressIP)
    username = request.data.get('username')
    # ---------

    # Validation
    if isBlocked:
        return Response({'error': 'Вы превысили лимит, повторите через 5 минут'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    if not username:
        return Response({'error': 'Укажите номер телефона'}, status=400)
    res = validateAndFormatPhoneNumber(username)
    if not res['success']:
        return Response({'error': res.get('error')}, status=400)

    username: str = res.get('formattedPhoneNumber')
    user = Customer.objects.filter(user__username=username).first()

    if not user:
        return Response({'error': 'Аккаунт еще не был создан'}, status=400)
    # ---------

    # Code send
    codeSendRes = sendCodeToPhone(username)
    code = codeSendRes.get('code')
    print('🚀 - code:', code)
    if not code:
        return codeSendRes
    # ---------

    resendLimiter.increment(addressIP)
    cacheKey = f'registration-code-{username[1:]}'

    cache.set(cacheKey, {
        **cache.get(cacheKey, {}),
        'code': code,
    }, TIME_DAY)

    return Response({
        "success": "На номер был отправлен новый звонок с кодом"
    })


@api_view(['POST'])
def registryConfirmView(request):
    # Get data
    addressIP = request.META.get('REMOTE_ADDR')
    username = request.data.get('username')
    supposedCode = request.data.get('supposedCode')
    isBlocked = registryConfirmLimiter.getIsBlocked(addressIP)
    # ---------

    # Validation
    if isBlocked:
        return Response({'error': 'Вы превысили лимит, повторите через час'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    if not username:
        return Response({"error": 'Укажите номер телефона'}, status=400)
    if not supposedCode:
        return Response({"error": 'Укажите предполагаемый код подтверждения'}, status=400)
    res = validateAndFormatPhoneNumber(username)
    if not res['success']:
        return Response({"error": res.get('error')}, status=400)

    username: str = res.get('formattedPhoneNumber')

    user = Customer.objects.filter(
        user__username=username
    ).first()
    if not user:
        return Response({'error': 'Аккаунт еще не был создан'}, status=400)
    # ---------
    cacheKey = f'registration-code-{username[1:]}'

    cacheObj = cache.get(cacheKey, {})
    code = cacheObj.pop('code', '')

    if str(code) == str(supposedCode):
        tokenTuple = Token.objects.get_or_create(user=user.user)
        cache.delete(cacheKey)
        return Response({
            'success': 'Номер телефона был подтвержден',
            'token': tokenTuple[0].key,
        })

    registryConfirmLimiter.increment(addressIP)
    return Response({'error': 'Код не подходит'}, status=400)
