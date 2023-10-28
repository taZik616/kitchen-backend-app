cd app
python manage.py makemigrations api --noinput
python manage.py makemigrations --noinput
python manage.py migrate
python manage.py migrate django_celery_results
python manage.py migrate django_celery_beat
python manage.py collectstatic --noinput

echo """
import settings.on_start_app
""" | python manage.py shell

# daphne -b 0.0.0.0 -p 8000 settings.asgi:application
python manage.py runserver 0.0.0.0:8000
