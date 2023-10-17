from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class City(models.Model):
    name = models.CharField('Название', max_length=100)

    phoneNumber = PhoneNumberField(verbose_name='Номер телефона')
    officeAddress = models.CharField('Адрес главного офиса', max_length=250)
    coordinates = models.JSONField('Координаты', null=True)

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.officeAddress}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
