# Generated by Django 3.0.8 on 2020-11-04 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20201011_1719'),
        ('inventory', '0030_auto_20201103_1641'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0010_auto_20201104_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', models.DateTimeField(verbose_name='Date')),
                ('invoice_number', models.CharField(max_length=20, unique=True, verbose_name='Invoice number')),
                ('total', models.FloatField(blank=True, default=0, null=True, verbose_name='Total')),
                ('slug', models.SlugField(default='')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer', verbose_name='Credit customer')),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceGoodsReturns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(null=True, verbose_name='Quantity')),
                ('price', models.FloatField(null=True, verbose_name='Selling price')),
                ('vat', models.FloatField(default=0, verbose_name='VAT')),
                ('amount', models.FloatField(default=0, verbose_name='Amount')),
                ('invoice_ref', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_items_set', to='sales.SalesInvoice')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_stock', to='inventory.Stock')),
                ('sale_item_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items', to='sales.SoldGoods')),
                ('unit_of_measurement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.UnitOfMeasurement')),
            ],
        ),
    ]