# Generated by Django 3.0.8 on 2020-10-23 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_auto_20201014_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='is_promotional',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='purchase_price',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='sales_discount',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='selling_price_1',
        ),
    ]
