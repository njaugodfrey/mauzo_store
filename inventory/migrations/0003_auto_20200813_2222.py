# Generated by Django 3.0.8 on 2020-08-13 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20200813_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitofmeasurement',
            name='stock',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='inventory.Stock'),
        ),
    ]
