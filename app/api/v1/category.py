from api.models import Category
from api.serializers import CategorySerializer
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView


class CategoriesView(ListAPIView):
    serializer_class = CategorySerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'name']
    ordering = ['id']

    def get_queryset(self):
        categories = Category.objects.all()

        return categories
