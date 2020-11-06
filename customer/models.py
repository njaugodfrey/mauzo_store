from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.

class Customer(models.Model):
    customer_code = models.CharField(
        verbose_name='Customer code', max_length=50,
        null=False, blank=False, unique=True,
        primary_key=True
    )
    customer_name = models.CharField(
        verbose_name='Common nickname', max_length=100
    )
    customer_full_name = models.CharField(
        verbose_name='Full name', max_length=100
    )
    phone_number = models.CharField(
        verbose_name='Phone number', max_length=12,
    )
    location = models.TextField(
        verbose_name='Customer address'
    )
    opening_balance = models.FloatField(
        verbose_name='Opening balance', blank=True,
        null=True
    )
    balance = models.FloatField(
        verbose_name='Balance', default=0
    )
    slug = models.SlugField(
        default=''
    )    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.customer_name)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.customer_name)


# class CashReceipt(models.Model):
#     receipt_number = models.CharField(
#         verbose_name='Receipt number',
#         max_length=20
#     )
#     payer = models.CharField(
#         verbose_name='Payer', null=True,
#         blank=True, max_length=50
#     )
#     customer = models.ForeignKey(
#         Customer, verbose_name='Customer',
#         null=True, blank=True, on_delete=models.CASCADE
#     )
#     """sales_ref = models.ManyToManyField(
#         SalesReceipt, verbose_name='Receipt', null=True,
#         blank=True
#     )"""
#     amount = models.FloatField(
#         verbose_name='Amount'
#     )
