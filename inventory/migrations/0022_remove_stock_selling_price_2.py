# Generated by Django 3.0.8 on 2020-10-11 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_auto_20201011_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='selling_price_2',
        ),
    ]
