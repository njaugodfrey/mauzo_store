# Generated by Django 3.1 on 2020-09-15 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20200913_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsreceipt',
            name='total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='goodsreturned',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
