from api.models import City
from rest_framework import serializers


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = City
