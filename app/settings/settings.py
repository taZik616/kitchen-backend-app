import warnings
from os import path
from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

env = Env()
env.read_env(BASE_DIR / '.env', recurse=False)

ALLOWED_HOSTS = ['89.108.99.39', 'po-obedai.ru',
                 'localhost', '127.0.0.1', '0.0.0.0']
CSRF_TRUSTED_ORIGINS = ['https://po-obedai.ru']

INSTALLED_APPS = [
    'daphne',  # В доках сказано в начало положить
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.postgres',
    'api.apps.ApiConfig',
    'django_jsonform',
    'jquery',
    'corsheaders',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'django_cleanup.apps.CleanupConfig',
    'floppyforms',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
CORS_ORIGIN_ALLOW_ALL = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'pyamqp://rabbitmq:5672'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

ROOT_URLCONF = 'settings.urls'
WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

with env.prefixed('DJANGO_'):
    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG', default=True)
    DATABASES = {
        'default': env.dj_db_url("DB_URL")
    }
    CACHES = {
        'default': env.dj_cache_url("CACHE_URL")
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SMS_RU_API_KEY = env.str('SMS_RU_API_KEY')

# Internationalization
LANGUAGE_CODE = 'ru-ru'
LANGUAGES = [
    ('ru', 'Русский'),
]

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = path.join(PROJECT_DIR, 'static')

MEDIA_ROOT = path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'api.BaseUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


warnings.filterwarnings('ignore', module='floppyforms',
                        message='Unable to import floppyforms.gis')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

ASGI_APPLICATION = "settings.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}
