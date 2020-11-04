from django.db import models


# Create your models here.

class vat(models.Model):
    vat_code = models.CharField(
        verbose_name='VAT code', max_length=1,
        unique=True, blank=False, null=False
    )
    code_name = models.CharField(
        verbose_name='VAT code name', max_length=10
    )
    code_percentage = models.IntegerField(
        verbose_name='VAT percentage'
    )

    def __str__(self):
        return '{}'.format(self.code_name)


class BankAccount(models.Model):
    account_name = models.CharField(
        max_length=20
    )
    bank_name = models.CharField(
        max_length=20
    )
