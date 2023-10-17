from api.models import ServerSetting
from api.serializers import ServerSettingSerializer
from rest_framework.generics import RetrieveAPIView


class SettingView(RetrieveAPIView):
    serializer_class = ServerSettingSerializer

    def get_object(self):
        return ServerSetting.objects.filter(isUsed=True).first()
