from api.models import BasketProduct, Customer, Product
from api.serializers.city import CitySerializer
from api.serializers.product import ProductSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class BaseUserCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CustomerSerializer(serializers.ModelSerializer):
    user = BaseUserCustomerSerializer()
    city = CitySerializer()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'user', 'city']


class BasketProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    productId = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    class Meta:
        model = BasketProduct
        fields = ['id', 'product', 'productId', 'quantity']

    def create(self, validated_data):
        productId = validated_data.pop('productId')
        customer = Customer.objects.get(user=self.context['request'].user)
        return BasketProduct.objects.create(
            product=productId, customer=customer, **validated_data)
