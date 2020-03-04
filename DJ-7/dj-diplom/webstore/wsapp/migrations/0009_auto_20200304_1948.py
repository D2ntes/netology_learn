# Generated by Django 3.0.2 on 2020-03-04 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wsapp', '0008_auto_20200227_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=30, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'verbose_name': 'Vendor', 'verbose_name_plural': 'Vendors'},
        ),
        migrations.AlterField(
            model_name='category',
            name='title_category',
            field=models.CharField(max_length=30, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='vendor',
            field=models.ManyToManyField(related_name='categories', to='wsapp.Vendor', verbose_name='Vendor'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount_prod',
            field=models.PositiveIntegerField(verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wsapp.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_prod',
            field=models.CharField(max_length=256, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_prod',
            field=models.ImageField(blank=True, null=True, upload_to='static/products/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_prod',
            field=models.CharField(max_length=64, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wsapp.Vendor', verbose_name='Vendor'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='title_vendor',
            field=models.CharField(max_length=30, verbose_name='Name'),
        ),
        migrations.CreateModel(
            name='DetailOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_do', models.PositiveIntegerField(verbose_name='Amount')),
                ('order', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wsapp.Order', verbose_name='Order')),
                ('person', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('product', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wsapp.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Detail of order',
                'verbose_name_plural': 'Details of order',
            },
        ),
        migrations.AddConstraint(
            model_name='detailorder',
            constraint=models.UniqueConstraint(fields=('person', 'product', 'order'), name='person_product_order'),
        ),
        migrations.AlterUniqueTogether(
            name='detailorder',
            unique_together={('person', 'product', 'order')},
        ),
    ]
