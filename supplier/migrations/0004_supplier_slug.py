# Generated by Django 3.1 on 2020-09-27 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0003_supplierpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
