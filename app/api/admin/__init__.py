from django.contrib import admin
from django.contrib.admin.sites import site

from .category import CategoryAdmin
from .city import CityAdmin
from .log_entry import LogEntryAdmin
from .product import ProductAdmin
from .server_setting import ServerSettingAdmin
from .support_request import SupportRequestAdmin
from .user import *

admin.site.site_title = "Сайт администрирования"
admin.site.site_header = "Сайт администрирования"

# При создании модели необходимо вписать ее название,
# чтобы упорядочить ее в списке моделей на сайте администратора
ADMIN_ORDERING = [
    ('api', [
        'Category',
        # Товары
        'Product',
        # Пользователи
        'BaseUser',
        'Customer',
        'SupportRequest',
        # # Покупки
        # 'BuyBalance',
        # 'BuyBalanceByCard',
        # 'Commission',
        # 'OnlineOrder',
        # Локации
        'City',
        # Некоторые дополнительные настройки
        'ServerSetting',
    ])
]


def custom_get_app_list(request, app_label=None, self=site):
    """
    На это я ухайдохал кучу времени, но оно работает теперь!
    Это для сортировки админки(по умолчанию идет просто по алфавиту, а не по логике)
    """
    app_dict = self._build_app_dict(request, app_label)
    modified_app_list = []

    for app_name, object_list in ADMIN_ORDERING:
        app = app_dict.get(app_name)
        if app:
            app_models = [model for model in app['models']
                          if model['object_name'] in object_list]
            app_models.sort(key=lambda x: object_list.index(x['object_name']))
            app['models'] = app_models
            modified_app_list.append(app)

    for app_name, app in app_dict.items():
        if app_name not in dict(ADMIN_ORDERING):
            modified_app_list.append(app)

    return modified_app_list


# Переопределить класс админ. сайта по умолчанию плохое решение(это отразиться на всех классах админ. сайтов), поэтому делаю так
site.get_app_list = custom_get_app_list
