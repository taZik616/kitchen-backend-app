
from django_ratelimit.decorators import ratelimit
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response


@ratelimit(key='ip', rate='10/min', block=False)
@api_view(['POST'])
def checkTokenView(request):
    token = request.data.get('token')
    try:
        Token.objects.get(key=token)
        return Response({'success': True})
    except Token.DoesNotExist:
        return Response({'success': False})
