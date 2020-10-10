from django.db import models
from django.template.defaultfilters import slugify
#from inventory.models import GoodsReceipt


# Create your models here.

class Supplier(models.Model):
    supplier_code = models.CharField(
        verbose_name='Supplier code', max_length=10,
        null=False, unique=True, blank=False,
        primary_key=True
    )
    supplier_name = models.CharField(
        verbose_name='Name', max_length=500,
        null=False, blank=False
    )
    contacts = models.TextField(
        verbose_name='Contacts'
    )
    pin = models.CharField(
        verbose_name='KRA PIN Number', max_length=11,
        unique=True, null=False, blank=False,
    )
    vat_number = models.CharField(
        verbose_name='VAT Number', max_length=10,
        null=True, blank=True, unique=True
    )
    slug = models.SlugField(
        default=''
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.supplier_name)
        super(Supplier, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.supplier_name)


class SupplierPayment(models.Model):
    payment_number = models.CharField(
        verbose_name='Reference', max_length=50
    )
    payer = models.CharField(
        verbose_name='Payee', null=True,
        blank=True, max_length=50
    )
    supplier = models.ForeignKey(
        Supplier, verbose_name='Supplier',
        null=True, blank=True, on_delete=models.CASCADE
    )
    """ supplies_ref = models.ManyToManyField(
        GoodsReceipt, verbose_name='Invoice/Reference', null=True,
        blank=True
    ) """
    amount = models.FloatField(
        verbose_name='Amount'
    )

