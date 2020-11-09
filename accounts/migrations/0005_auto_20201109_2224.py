# Generated by Django 3.0.8 on 2020-11-09 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_auto_20201106_1513'),
        ('accounts', '0004_cashaccount_cashreceipt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cashreceipt',
            old_name='amount',
            new_name='total',
        ),
        migrations.RemoveField(
            model_name='cashreceipt',
            name='invoice',
        ),
        migrations.AddField(
            model_name='cashreceipt',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.CreateModel(
            name='CashReceiptItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Item description')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.SalesInvoice')),
                ('receipt_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.CashReceipt')),
            ],
        ),
    ]
