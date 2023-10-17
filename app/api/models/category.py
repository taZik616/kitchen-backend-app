from django.db import models


class Category(models.Model):
    name = models.CharField(
        default='', max_length=100,
        unique=True,  verbose_name='Название')
    previewImage = models.ImageField(
        upload_to='category-images/', blank=True, null=True, verbose_name="Превью-картинка",
        help_text="Соотношение сторон(aspect ratio) = 1.5. Пример правильной пропорции картинки: ширина=150 и высота=100"
    )
    slug = models.SlugField(
        'Слаг', max_length=100, unique=True, null=False,
        help_text='Короткое название-идентификатор на англ, без пробелов и спец символов')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.pk} - {self.name}'
