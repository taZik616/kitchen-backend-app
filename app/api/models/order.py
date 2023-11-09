import math

from api.constants import ORDER_STATUSES, PAYMENT_METHODS
from django.db import models
from django.db.models import F, IntegerField, Sum
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    customer = models.ForeignKey(
        'api.Customer', models.SET_NULL, null=True,
        verbose_name='Покупатель')
    city = models.ForeignKey(
        'api.City', models.SET_NULL, null=True, verbose_name='Город')
    address = models.JSONField(
        'Адрес', null=True, blank=True, default=None)

    status = models.CharField(
        'Статус', choices=ORDER_STATUSES, default='notPaid')
    paymentMethod = models.CharField('Метод оплаты', choices=PAYMENT_METHODS)
    confirmationToken = models.CharField(
        'Токен для оплаты', max_length=500, null=True, blank=True)
    useBonuses = models.BooleanField('Были использованы бонусы', default=False)

    createdAt = models.DateTimeField('Дата создания', auto_now_add=True)
    updatedAt = models.DateTimeField(
        'Дата последнего обновления', auto_now=True)

    @property
    def totalPrice(self):
        total = self.orderproduct_set.annotate(
            total_price=F('quantity') * F('productInfo__price')
        ).aggregate(
            total=Sum('total_price', output_field=IntegerField())
        )['total']
        return math.ceil(total) if total else 0

    @property
    def productsCount(self):
        return self.orderproduct_set.count()

    class Meta:
        verbose_name = 'Онлайн заказ'
        verbose_name_plural = 'Онлайн заказы'

    def __str__(self):
        username = self.customer.user.username if self.customer else "-"
        return f'{self.pk} - Пользователь: {username}; Цена: {self.totalPrice}; Статус: {self.status}'


class OrderProduct(models.Model):
    product = models.ForeignKey(
        'api.Product', models.SET_NULL, null=True, verbose_name='Товар')
    productInfo = models.ForeignKey(
        'api.ProductInfoInCity', models.SET_NULL, null=True, verbose_name='Инфо о товаре')
    quantity = models.PositiveIntegerField('Количество')
    order = models.ForeignKey(Order, models.CASCADE, verbose_name='Заказ')

    class Meta:
        verbose_name = 'Товар из заказа'
        verbose_name_plural = 'Товары из заказа'

    def __str__(self):
        prodId = self.product.pk if self.product else "<None>"

        return f'{self.pk} - Товар: ID({prodId}); Кол-во: {self.quantity}; Заказ №{self.order.pk}'
