from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Product(models.Model):
    title_prod = models.CharField(max_length=64, verbose_name='Name', )
    description_prod = models.CharField(verbose_name='Description', max_length=256, )
    amount_prod = models.PositiveIntegerField(verbose_name='Amount', )
    image_prod = models.ImageField(null=True, blank=True, upload_to='static/products/', verbose_name='Image',)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Category')
    vendor = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Vendor')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title_prod


class Article(models.Model):
    title_art = models.CharField(max_length=128, verbose_name='Название',)
    description_art = models.TextField(max_length=3000, default='', verbose_name='Описание', )
    published_at = models.DateTimeField(default=now, editable=True, verbose_name='Дата публикации',)
    products = models.ManyToManyField('Product', related_name='articles',)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title_art


class Category(models.Model):
    title_category = models.CharField(max_length=30, verbose_name='Name', )
    vendor = models.ManyToManyField('Vendor', related_name='categories', verbose_name='Vendor')

    def get_vendors(self):
        return ",".join([str(p) for p in self.vendor.all()])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title_category


class Vendor(models.Model):
    title_vendor = models.CharField(max_length=30, verbose_name='Name', )

    def get_parents(self):
        return ",".join([str(p) for p in self.parent.all()])

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return self.title_vendor


class Order(models.Model):
    status = models.CharField(max_length=30, verbose_name='Status', )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return str(self.pk)


class DetailOrder(models.Model):
    amount_do = models.PositiveIntegerField(verbose_name='Amount', )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, db_index=False, null=True, blank=True, verbose_name='Product')
    person = models.ForeignKey(User, on_delete=models.CASCADE, db_index=False, null=True, blank=True, verbose_name='User')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, db_index=False, null=True, blank=True, verbose_name='Order')

    class Meta:
        verbose_name = 'Detail of order'
        verbose_name_plural = 'Details of order'
        unique_together = ('person', 'product', 'order')
        constraints = [
            models.UniqueConstraint(fields=['person', 'product', 'order'], name='person_product_order'),
        ]
