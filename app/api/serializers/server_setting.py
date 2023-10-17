from api.models.server_setting import HelpfulInfo, ServerSetting
from rest_framework import serializers


class HelpfulInfoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpfulInfo
        fields = ['key', 'title']


class HelpfulInfoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpfulInfo
        fields = ['key', 'title', 'markdownContent']


class ServerSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerSetting
        fields = ['defaultUserCashbackPercent']
