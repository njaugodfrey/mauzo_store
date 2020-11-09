from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from customer import models as customers
from sales.models import SalesInvoice


class CashAccount(models.Model):
    account_name = models.CharField(
        max_length=20
    )


class CashReceipt(models.Model):
    receipt_date = models.DateField(
        verbose_name='Date'
    )
    receipt_number = models.CharField(
        verbose_name='Receipt Number',  max_length=50,
        unique=True
    )
    description = models.TextField(
        verbose_name='Description', blank=True,
        null=True
    )
    customer = models.ForeignKey(
        customers.Customer, on_delete=models.CASCADE,
        null=True, blank=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True
    )
    total = models.FloatField(
        verbose_name='Amount'
    )
    slug = models.SlugField(
        default=''
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.receipt_number)
        super(CashReceipt, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.receipt_number)


class CashReceiptItems(models.Model):
    receipt_ref = models.ForeignKey(
        CashReceipt, on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        SalesInvoice, on_delete=models.CASCADE,
        blank=True, null=True
    )
    description = models.CharField(
        verbose_name='Item description',
        null=True, blank=True, max_length=250
    )
    amount = models.FloatField
