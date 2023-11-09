from api.models import Customer, Product, ProductImage, ProductInfoInCity
from api.serializers.category import CategorySerializer
from rest_framework import serializers

LITE_FIELDS = [
    'id', 'name', 'article', 'isHiddenInMarket', 'description', 'category',
    'weight', 'images', 'info'
]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('priority', 'image')


class ProductInfoInCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfoInCity
        fields = ['initialPrice', 'discountPercent', 'price']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True)
    info = ProductInfoInCitySerializer()

    class Meta:
        model = Product
        fields = LITE_FIELDS

    def to_representation(self, instance):
        images = ProductImage.objects.filter(product=instance)
        instance.images = sorted(
            images,
            key=lambda image: image.priority
        )

        request = self.context.get('request')
        customer = Customer.objects.get(user=request.user)
        instance.info = ProductInfoInCity.objects.filter(
            product__pk=instance.pk, city=customer.city).first()

        return super().to_representation(instance)


# class ProductDetailSerializer(ProductSerializer):
#     class Meta:
#         model = Product
#         fields = [*LITE_FIELDS, ]
