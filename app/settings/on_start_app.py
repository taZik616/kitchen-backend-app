from settings.settings import env

from django.contrib.auth import get_user_model

User = get_user_model()

with env.prefixed(f'SUPERUSER_'):
    username = env.str('USERNAME')
    password = env.str('PASSWORD')

    # Base user
    userInstance = User.objects.filter(username=username).first()
    if not userInstance:
        User.objects.create_superuser(username=username, password=password)
