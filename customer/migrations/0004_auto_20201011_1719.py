# Generated by Django 3.0.8 on 2020-10-11 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customer_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.FloatField(default=0, verbose_name='Balance'),
        ),
    ]
