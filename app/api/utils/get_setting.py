from api.constants import SETTINGS_ERROR
from api.models import ServerSetting


def getSetting():
    setting = ServerSetting.objects.filter(isUsed=True).first()
    if setting:
        return setting
    else:
        return {'error': SETTINGS_ERROR}
