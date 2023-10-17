from api.constants import SETTINGS_ERROR
from api.models import ServerSetting


def getSetting():
    '''
    Словарь с `['secretKey']` `['shopId']`
    '''
    setting = ServerSetting.objects.filter(isUsed=True).first()
    if setting:
        return setting
    else:
        return {'error': SETTINGS_ERROR}
