# Generated by Django 5.2 on 2025-05-09 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zenitsu_shop', '0002_alter_order_delivery_alter_order_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='zenitsu_shop.category'),
        ),
    ]
