from django.db import models


# Create your models here.

class Company(models.Model):
    company_name = models.CharField(
        verbose_name='Name', max_length=30
    )
    postal_address = models.TextField(
        verbose_name='Postal Address'
    )
    telephone_1 = models.CharField(
        verbose_name='Telephone 1', max_length=14
    )
    telephone_2 = models.CharField(
        verbose_name='Telephone 2', blank=True,
        null=True, max_length=14
    )
    kra_pin = models.CharField(
        verbose_name='Company PIN number', max_length=11
    )
    kra_vat = models.CharField(
        verbose_name='Company VAT number', max_length=10
    )
