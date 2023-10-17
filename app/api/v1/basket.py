from api.decorators import onlyCustomer
from api.models import BasketProduct, Customer
from api.serializers import BasketProductSerializer
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BasketView(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketProductSerializer

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return BasketProduct.objects.filter(customer=customer)

    def get_object(self):
        productId = self.request.GET.get('productId')
        customer = Customer.objects.get(user=self.request.user)
        return BasketProduct.objects.filter(customer=customer, product__id=productId).first()

    @method_decorator(onlyCustomer)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @method_decorator(onlyCustomer)
    def put(self, request, *args, **kwargs):
        productId = request.data.get('productId')
        if self.get_queryset().filter(product__id=productId).exists():
            return Response({'error': 'Товар уже в корзине'}, status=400)
        return self.create(request, *args, **kwargs)

    @method_decorator(onlyCustomer)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@onlyCustomer
def clearBasket(request, customer):
    try:
        BasketProduct.objects.filter(customer=customer).delete()
        return Response({
            'success': 'Ваша корзина была успешно очищена'
        })
    except:
        return Response({'error': 'Не удалось очистить корзину'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@onlyCustomer
def basketSetCount(request, customer):
    try:
        productId = request.data.get('productId')
        count = request.data.get('count')
        productInBasket = BasketProduct.objects.filter(
            customer=customer, product__id=productId).first()
        if productInBasket:
            productInBasket.quantity = count
            productInBasket.save()
        return Response({
            'success': 'Счетчик был успешно обновлен'
        })
    except:
        return Response({'error': 'Не удалось обновить счетчик'}, status=400)
