from typing import Any

from api.decorators import onlyCustomer
from api.models import Product, ProductInfoInCity
from api.serializers import ProductSerializer
from api.v1.common import CustomPagination
from django.db import models
from django.db.models import Q, Subquery
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

    def list(self, request, *args, **kwargs):
        customer = kwargs['customer']
        queryset = self.filter_queryset(Product.objects.filter(isHiddenInMarket=False).filter(
            Q(productinfoincity__city=customer.city) & ~Q(
                productinfoincity__product=None)
        ).distinct())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(onlyCustomer)
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
