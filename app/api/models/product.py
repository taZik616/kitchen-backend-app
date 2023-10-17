import random
from os import path

from django.db import models


def randomArticle():
    return ''.join(random.choices('0123456789', k=10))


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название')
    article = models.CharField(
        'Артикул', unique=True,
        default=randomArticle, max_length=100)

    isHiddenInMarket = models.BooleanField(
        default=False, verbose_name='Снять с продажи')
    description = models.TextField('Описание', blank=True, max_length=2000)

    category = models.ForeignKey(
        'api.Category', on_delete=models.CASCADE, verbose_name='Категория')
    weight = models.PositiveIntegerField(
        'Вес', help_text='Указывается в граммах')

    createdAt = models.DateTimeField('Дата создания', auto_now_add=True)
    updatedAt = models.DateTimeField(
        'Дата последнего обновления', auto_now=True)

    def __str__(self):
        return f'ID({self.pk}) - {self.name}; Арт.{self.article}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        permissions = [
            ("change_hidden_in_market",
             "Возможность снимать с продажи товары"),
        ]


class ProductImage(models.Model):
    priority = models.PositiveIntegerField(
        verbose_name='Порядковый номер картинки')
    image = models.ImageField(
        upload_to='product-images/', verbose_name='Картинка')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Товар')

    class Meta:
        verbose_name = 'Картинка товара'
        verbose_name_plural = 'Картинки товаров'
        # Это уникальное ограничение гарантирует, что комбинация product и priority будет уникальной для каждого объекта
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'priority'],
                name='unique_product_image_priority',
                violation_error_message='Порядковый номер картинки должен быть уникальным в контексте одного товара.'
            )
        ]

    def __str__(self):
        return f'Картинка: {path.basename(self.image.path)}, товар {self.product.pk}'


class ProductInfoInCity(models.Model):
    city = models.ForeignKey('api.City', models.CASCADE, verbose_name='Город')

    initialPrice = models.PositiveIntegerField(verbose_name="Цена (₽)")
    discountPercent = models.PositiveIntegerField('Процент скидки', default=0)
    price = models.PositiveIntegerField(
        'Итоговая цена (₽)', editable=False)

    product = models.ForeignKey(
        'api.Product', models.CASCADE, verbose_name='Товар')

    def save(self, *args, **kwargs):
        self.price = round(self.initialPrice -
                           (self.initialPrice * self.discountPercent) / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'ID({self.pk}); Арт.{self.product.article if self.product else "НЕТУ"}; - {self.price} ₽; '

    class Meta:
        verbose_name = 'Данные о товаре для города'
        verbose_name_plural = 'Данные о товаре для городов'
