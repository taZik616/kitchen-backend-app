from settings.settings import (
    YOOKASSA_SECRET_KEY,
    YOOKASSA_SHOP_ID,
    YOOKASSA_TEST_SECRET_KEY,
    YOOKASSA_TEST_SHOP_ID,
)

SETTINGS_ERROR = 'На сервере возникла проблема с настройками'

TIME_HOUR = 60*60
TIME_DAY = 60*60*24

ORDER_STATUSES = (
    ('notPaid', 'Не оплачен'),
    ('alreadyPaid', 'Оплачен'),
    ('preparing', 'Приготовляется'),
    ('delivered', 'Доставляется'),
    ('received', 'Получен'),
    ('canceled', 'Отменен'),
)

PAYMENT_METHODS = (
    ('online', 'В приложении онлайн'),
    ('card', 'Банковской картой'),
    ('cash', 'Наличными')
)
PAYMENT_METHODS_ARRAY = [reason[0] for reason in PAYMENT_METHODS]


def getYookassaSchema(isTest: bool):
    return {
        'type': 'dict',
        'keys': {
            'shopId': {
                'type': 'number',
                'title': 'Shop ID',
                'required': True,
                'placeholder': '123456',
                'default': YOOKASSA_TEST_SHOP_ID if isTest else YOOKASSA_SHOP_ID,
                'helpText': 'Идентификатор магазина из профиля юкассы'
            },
            'secretKey': {
                'type': 'string',
                'title': 'Секретный ключ',
                'required': True,
                'placeholder': 'prefix_xxxxx',
                'default': YOOKASSA_TEST_SECRET_KEY if isTest else YOOKASSA_SECRET_KEY,
                'helpText': 'Секретный ключ принадлежащий идентификатору магазина'
            },
        }
    }


YOOKASSA_TEST_ACQUIRING_SCHEMA = getYookassaSchema(isTest=True)

YOOKASSA_ACQUIRING_SCHEMA = getYookassaSchema(isTest=False)
