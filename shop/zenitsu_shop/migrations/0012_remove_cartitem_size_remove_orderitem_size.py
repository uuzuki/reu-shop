# Generated by Django 5.2 on 2025-05-12 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zenitsu_shop', '0011_cartitem_size_orderitem_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
    ]
