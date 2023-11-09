from typing import Any

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
    defaultAddress = models.ForeignKey(
        'api.CustomerAddress', models.SET_NULL, null=True, blank=True,
        verbose_name='Избранный адрес(по умолчанию)', related_name='defaultAddress')

    city = models.ForeignKey(
        'api.City', models.SET_NULL, null=True, verbose_name='Город')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f"{self.user.username}, {self.name}"


class CustomerAddress(models.Model):
    city = models.ForeignKey(
        'api.City', models.SET_NULL, null=True, verbose_name='Город')
    customer = models.ForeignKey(
        'api.Customer', null=True, on_delete=models.SET_NULL, verbose_name='Пользователь')

    streetAndHouse = models.CharField(
        'Улица, дом', max_length=300, default='')
    entrance = models.CharField(
        'Подъезд', max_length=10, null=True, blank=True, default='')
    floor = models.CharField(
        'Этаж', max_length=10, null=True, blank=True, default='')
    flat = models.CharField(
        'Квартира', max_length=10, null=True, blank=True, default='')
    hasBeenDeleted = models.BooleanField(
        'Был удален', default=False,
        help_text='Если пользователь удаляет адрес но он есть в заказе то адрес \
благодаря флагу останется в БД без отмены удаления у пользователя')

    comment = models.TextField(
        'Комментарий', null=True, blank=True, max_length=500)

    coords = models.JSONField('Координаты')

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f"{self.pk}, {self.customer.user.username}, {self.city.name} - {self.streetAndHouse}, кв. {self.flat}"


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
