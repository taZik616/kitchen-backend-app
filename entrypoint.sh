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

uvicorn settings.fast_api:app --proxy-headers --host 0.0.0.0 --port 8000 --reload
# python manage.py runserver 0.0.0.0:8000
