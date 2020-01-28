from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Product(models.Model):
    title_prod = models.CharField(max_length=30, verbose_name='Название', )
    description_prod = models.CharField(max_length=100, verbose_name='Описание', )
    amount_prod = models.PositiveIntegerField(verbose_name='Количество', )
    image_prod = models.ImageField(null=True, blank=True, upload_to='static/products/', verbose_name='Изображение',)
    # subtype = models.ForeignKey(Subtype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Подтип')
    # type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title_prod


class Article(models.Model):
    title_art = models.CharField(max_length=64, verbose_name='Название',)
    description_art = models.CharField(max_length=254, default='', verbose_name='Описание', )
    published_at = models.DateTimeField(default=now, editable=True, verbose_name='Дата публикации')
    products = models.ManyToManyField(Product, related_name='articles')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title_art