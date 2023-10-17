import requests
from api.constants import SETTINGS_ERROR
from api.models import ServerSetting


def sendCodeToPhone(phoneNumber):
    setting = ServerSetting.objects.filter(isUsed=True).first()
    if not setting:
        return {'error': SETTINGS_ERROR}
    smsResponse = requests.post(
        f'https://sms.ru/code/call?phone={phoneNumber}&ip=-1&api_id={setting.sms_ru_api_key}'
    )

    if smsResponse.status_code != 200:
        return {"error": "На этот номер не удалось отправить звонок с кодом"}

    dataSmsRu = smsResponse.json()
    status = dataSmsRu.get('status')
    code = dataSmsRu.get('code')

    if status != 'OK' or not code:
        return {"error": "На этот номер не удалось отправить звонок с кодом"}
    return {'code': code}
