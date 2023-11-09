from api.models import Order, OrderProduct
from rest_framework import serializers

from .city import CitySerializer
from .product import ProductInfoInCitySerializer, ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    totalPrice = serializers.SerializerMethodField()

    def get_totalPrice(self, obj):
        return obj.totalPrice

    class Meta:
        exclude = [
            'customer', 'city', 'address', 'updatedAt']
        model = Order


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    productInfo = ProductInfoInCitySerializer()

    class Meta:
        exclude = ['order']
        model = OrderProduct


class OrderDetailSerializer(OrderSerializer):
    products = OrderProductSerializer(many=True)
    city = CitySerializer()

    class Meta:
        exclude = ['customer', 'updatedAt']
        model = Order

    def to_representation(self, instance):
        instance.products = OrderProduct.objects.filter(
            order=instance)
        return super().to_representation(instance)
