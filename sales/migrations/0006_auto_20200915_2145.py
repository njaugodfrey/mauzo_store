# Generated by Django 3.1 on 2020-09-15 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20200909_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesreceiptvoid',
            name='vat',
            field=models.FloatField(default=0, verbose_name='VAT'),
        ),
        migrations.AddField(
            model_name='soldgoods',
            name='vat',
            field=models.FloatField(default=0, verbose_name='VAT'),
        ),
    ]
