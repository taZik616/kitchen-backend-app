from django.db import models


class SupportRequest(models.Model):
    customer = models.ForeignKey(
        'api.Customer', models.SET_NULL, null=True, verbose_name='Пользователь')
    message = models.TextField('Сообщение')

    createdAt = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.pk} - {self.customer.name if self.customer else "<None>"}'

    class Meta:
        verbose_name = 'Запрос поддержки'
        verbose_name_plural = 'Запросы поддержки'
