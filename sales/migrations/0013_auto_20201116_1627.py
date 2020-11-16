# Generated by Django 3.1.2 on 2020-11-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_auto_20201106_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesreceipt',
            name='is_cleared',
            field=models.BooleanField(default=False, verbose_name='Cleared'),
        ),
        migrations.AddField(
            model_name='salesreceipt',
            name='printed',
            field=models.BooleanField(default=False, verbose_name='Printed Receipt'),
        ),
        migrations.AlterField(
            model_name='salesreceipt',
            name='is_credit',
            field=models.BooleanField(default=False, verbose_name='Temporary credit'),
        ),
    ]
