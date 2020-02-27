from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Product(models.Model):
    title_prod = models.CharField(max_length=64, verbose_name='Название', )
    description_prod = models.CharField(verbose_name='Описание', max_length=256, )
    amount_prod = models.PositiveIntegerField(verbose_name='Количество', )
    image_prod = models.ImageField(null=True, blank=True, upload_to='static/products/', verbose_name='Изображение',)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    vendor = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Производитель')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title_prod


class Article(models.Model):
    title_art = models.CharField(max_length=128, verbose_name='Название',)
    description_art = models.TextField(max_length=3000, default='', verbose_name='Описание', )
    published_at = models.DateTimeField(default=now, editable=True, verbose_name='Дата публикации',)
    products = models.ManyToManyField('Product', related_name='articles',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title_art


class Category(models.Model):
    title_category = models.CharField(max_length=30, verbose_name='Название', )
    # vendor = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Производитель')
    vendor = models.ManyToManyField('Vendor', related_name='categories', verbose_name='Производитель')

    def get_vendors(self):
        return ",".join([str(p) for p in self.vendor.all()])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title_category


class Vendor(models.Model):
    title_vendor = models.CharField(max_length=30, verbose_name='Название', )
    # category = models.ManyToManyField('Category', related_name='vendors', verbose_name='Категория')

    def get_parents(self):
        return ",".join([str(p) for p in self.parent.all()])

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.title_vendor
