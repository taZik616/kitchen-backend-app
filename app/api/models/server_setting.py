from django.db import models
from settings.settings import SMS_RU_API_KEY


class ServerSetting(models.Model):
    sms_ru_api_key = models.CharField(default=SMS_RU_API_KEY, max_length=125)

    defaultUserCashbackPercent = models.DecimalField(
        'Процент который начисляется баллами с каждой покупки (%)',
        default=1, decimal_places=2, max_digits=5,
        help_text='Бонусы зачисляются только натуральными числами')

    isUsed = models.BooleanField(
        default=True, verbose_name='Используется клиент-приложениями')

    def __str__(self):
        return f"{self.pk} - Используются клиент-приложениями: [{'ДА' if self.isUsed else 'НЕТ'}]"

    class Meta:
        verbose_name = 'Настройки сервера'
        verbose_name_plural = 'Настройка сервера'


HELPFUL_INFO_ICONS = [
    ('book', 'Книга'),
    ('star', 'Звездочка'),
    ('lock', 'Дверной замок'),
]


class HelpfulInfo(models.Model):
    key = models.CharField(
        max_length=200, unique=True, primary_key=True, verbose_name='Ключ', help_text='Ключи используются для собственной идентификации markdown контента в запросе <code>api/v1/info/{ключ}</code>')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    icon = models.CharField(
        'Иконка возле пункта в приложении', choices=HELPFUL_INFO_ICONS,
        null=True, blank=True)

    markdownContent = models.TextField(help_text='''
MarkDown используется для улучшения вида страниц с информацией, работает как уникальная разметка, которая может эффективно обрабатываться как в web среде, так и в мобильных приложениях<br>
Подробнее можно узнать в <a href="https://gist.github.com/Jekins/2bf2d0638163f1294637">этой статье</a><br>
Рекомендую использовать какой-либо онлайн редактор MarkDown, чтобы написать текст и вставить его сюда(к примеру <a href="https://stackedit.io">stackedit.io</a><br>)
''', verbose_name='Контент в MarkDown формате')

    serverSetting = models.ForeignKey(
        'api.ServerSetting', models.CASCADE,
        verbose_name='Связанные настройки')

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Полезная информация'
        verbose_name_plural = 'Отдел полезной информации'
