# Generated by Django 3.1 on 2020-09-13 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20200913_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitofmeasurement',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
