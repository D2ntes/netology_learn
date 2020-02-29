# Generated by Django 3.0.2 on 2020-02-26 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsapp', '0002_auto_20200227_0050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wsapp.Vendor', verbose_name='Производитель'),
        ),
    ]
