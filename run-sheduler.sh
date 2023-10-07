cd app
celery -A settings beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler