# Generated by Django 3.1 on 2020-09-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_cashreceipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
