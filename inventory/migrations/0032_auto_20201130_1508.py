# Generated by Django 3.1.2 on 2020-11-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0031_auto_20201116_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='unit_name',
            field=models.CharField(default='unit', max_length=10, verbose_name='Base unit name'),
        ),
    ]
