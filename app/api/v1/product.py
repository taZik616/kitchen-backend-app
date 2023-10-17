from typing import Any

from api.decorators import onlyCustomer
from api.models import Product
from api.serializers import ProductSerializer
from api.v1.common import CustomPagination
from django.utils.decorators import method_decorator
from django_filters.rest_framework import CharFilter, DjangoFilterBackend, FilterSet
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class ProductFilter(FilterSet):
    categoryId = CharFilter('category__id')

    class Meta:
        model = Product
        fields = ['categoryId']


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = [
        'name', 'price', 'createdAt', 'updatedAt', 'viewCounter',
        'salesCounter', 'rating']
    filterset_class = ProductFilter

    def get_queryset(self):
        items = Product.objects.filter(isHiddenInMarket=False)
        return items

    @method_decorator(onlyCustomer)
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
