from api.models import BaseUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changePasswordView(request):
    """Для того чтобы получить токен нужны поля `username` и `password`"""
    password = request.data.get('password')
    newPassword = request.data.get('newPassword')
    try:
        user: BaseUser = request.user

        if not user.check_password(password):
            return Response({'notMatch': 'Пароль от аккаунта и введенный не совпадают'}, status=400)
        if not newPassword:
            return Response({'error': 'Укажите новый пароль'}, status=400)
        try:
            validate_password(newPassword)
        except ValidationError as e:
            # Тут просто массив двумерный возвращается
            flattenedErrorList = [
                item for sublist in e.error_list for item in sublist]
            return Response({'passwordErrors': flattenedErrorList}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user.set_password(newPassword)
        # save() реально стоит вызывать, иначе не сохраняется новый пароль
        user.save()
        return Response({'success': 'Пароль успешно изменен!'})
    except:
        return Response({"error": 'Не удалось сменить пароль'}, status=400)
