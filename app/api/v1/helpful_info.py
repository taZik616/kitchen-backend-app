from api.models import HelpfulInfo, ServerSetting
from api.serializers import HelpfulInfoDetailSerializer, HelpfulInfoListSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


class HelpfulInfoListView(ListAPIView):
    serializer_class = HelpfulInfoListSerializer

    def get_queryset(self):
        return HelpfulInfo.objects.all()


class HelpfulInfoDetailView(RetrieveAPIView):
    serializer_class = HelpfulInfoDetailSerializer
    lookup_field = 'key'

    def get_queryset(self):
        setting = ServerSetting.objects.filter(isUsed=True).first()
        if not setting:
            return HelpfulInfo.objects.none()
        return HelpfulInfo.objects.filter(serverSetting=setting)
