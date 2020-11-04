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
    customer = models.ForeignKey(
        customers.Customer, on_delete=models.CASCADE,
        null=True, blank=True
    )
    invoice = models.ForeignKey(
        SalesInvoice, on_delete=models.CASCADE,
        null=True, blank=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True
    )
    amount = models.FloatField(
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
