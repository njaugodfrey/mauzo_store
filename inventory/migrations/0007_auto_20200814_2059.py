# Generated by Django 3.0.8 on 2020-08-14 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20200813_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Stock in hand'),
        ),
        migrations.AlterField(
            model_name='unitofmeasurement',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Stock'),
        ),
    ]
