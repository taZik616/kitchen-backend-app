from api.models.server_setting import HelpfulInfo, ServerSetting
from rest_framework import serializers


class HelpfulInfoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpfulInfo
        fields = ['key', 'title', 'icon']


class HelpfulInfoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpfulInfo
        fields = ['key', 'title', 'icon', 'markdownContent']


class ServerSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerSetting
        fields = ['defaultUserCashbackPercent']
