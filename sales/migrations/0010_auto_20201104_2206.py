# Generated by Django 3.0.8 on 2020-11-04 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_auto_20201007_2057'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CreditNote',
        ),
        migrations.DeleteModel(
            name='SalesInvoice',
        ),
    ]