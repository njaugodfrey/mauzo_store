# Generated by Django 3.0.8 on 2020-11-04 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_bankaccount_cashaccount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CashAccount',
        ),
    ]
