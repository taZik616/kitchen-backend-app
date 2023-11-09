from typing import Any

from api.decorators import onlyCustomer
from api.models import Order
from api.serializers import OrderDetailSerializer, OrderSerializer
from api.v1.common import CustomPagination
from django.utils.decorators import method_decorator
from pytils.numeral import get_plural
from rest_framework import filters, permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

# from django.db.models import Q
# class OrderFilter(FilterSet):
#     isCompleted = BooleanFilter(method='filterIsCompleted')

#     def filterIsCompleted(self, queryset, name, value):
#         completedStatuses = ['received', 'canceled', 'movedToAnotherOrder']
#         if value == True:
#             return queryset.filter(status__in=completedStatuses)
#         elif value == False:
#             return queryset.filter(~Q(status__in=completedStatuses))
#         return queryset

#     class Meta:
#         model = Order
#         fields = ['isCompleted']


class Pagination(CustomPagination):
    page_size = 30
    max_page_size = 60

    def get_paginated_response_schema(self, *args, **kwargs):
        schema = super().get_paginated_response_schema(*args, **kwargs)
        schema['properties']['countText'] = {
            'type': 'string',
            'example': '1 заказ',
        }
        return schema

    def get_paginated_response(self, *args, **kwargs):
        response = super().get_paginated_response(
            *args, **kwargs)
        response.data['countText'] = get_plural(
            self.page.paginator.count, u'заказ, заказа, заказов', absence=u"Заказов нет")
        return response


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = Pagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['createdAt']
    ordering = ['-createdAt']

    def get_queryset(self):
        return Order.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(customer=kwargs['customer'])
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        serialized = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serialized.data)

        return response

    @method_decorator(onlyCustomer)
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)


class OwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли текущий пользователь создателем объекта
        return obj.customer.user == request.user


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'
    permission_classes = [OwnerReadOnly]
