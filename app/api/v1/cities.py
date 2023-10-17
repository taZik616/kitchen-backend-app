from api.models import City
from api.serializers import CitySerializer
from rest_framework.generics import ListAPIView


class CityListView(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.all()
