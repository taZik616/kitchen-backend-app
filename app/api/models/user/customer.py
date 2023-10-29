import random

from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    user = models.OneToOneField(
        'api.BaseUser', models.CASCADE, verbose_name='Пользователь')
    isPhoneNumberVerified = models.BooleanField(
        default=False, blank=True, verbose_name="Подтвержденный номер")
    name = models.CharField('Имя', max_length=150)
    bonuses = models.IntegerField('Бонусы', default=0)
    awaitingDeletion = models.BooleanField('Ожидает удаления', default=False)
    deletionStartDate = models.DateTimeField(
        'Дата старта удаления', blank=True, null=True, default=None,
        help_text='Чтобы аккаунт удалился нужно 30 дней')

    city = models.ForeignKey(
        'api.City', models.SET_NULL, null=True, verbose_name='Город')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f"{self.user.username}, {self.name}"


class BasketProduct(models.Model):
    product = models.ForeignKey(
        'api.Product', models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Кол-во', default=1)
    customer = models.ForeignKey(
        'api.Customer', on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f"{self.customer.user.username}, {self.product.name} - {self.quantity} шт."
