from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from inventory import models as products
from customer import models as customers


# Create your models here.

class SalesReceipt(models.Model):
    sale_date = models.DateTimeField(
        verbose_name='Date'
    )
    receipt_number = models.CharField(
        verbose_name='Receipt number', max_length=20,
        unique=True
    )
    walkin_customer = models.CharField(
        verbose_name='Walk in Customer', null=True,
        blank=True, max_length=20
    )
    debtors_account = models.ForeignKey(
        customers.Customer, on_delete=models.CASCADE,
        verbose_name='Credit customer', null=True, blank=True
    )
    salesman = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    total = models.FloatField(
        verbose_name='Total', blank=True, null=True,
        default=0
    )
    is_credit = models.BooleanField(
        verbose_name='Temporary credit', default=False
    )
    is_cleared = models.BooleanField(
        verbose_name='Cleared', default=False
    )
    printed = models.BooleanField(
        verbose_name='Printed Receipt', default=False
    )
    slug = models.SlugField(
        default=''
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.receipt_number)
        super(SalesReceipt, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.receipt_number)


class SoldGoods (models.Model):
    receipt_ref = models.ForeignKey(
        SalesReceipt, on_delete=models.PROTECT,
        related_name='items_set'
    )
    product = models.ForeignKey(
        products.Stock, related_name='stock_item',
        on_delete=models.PROTECT    
    )
    unit_of_measurement = models.ForeignKey(
        products.UnitOfMeasurement, on_delete=models.CASCADE,
        null=True
    )
    quantity = models.FloatField(
        verbose_name='Quantity', null=False,
        blank=False
    )
    price = models.FloatField(
        verbose_name='Selling price'
    )
    vat = models.FloatField(
        verbose_name='VAT', default=0
    )
    amount = models.FloatField(
        verbose_name='Amount', default=0
    )
    void_sale = models.BooleanField(
        verbose_name='Void item sale', null=True,
        blank=True
    )


class SalesReceiptVoid(models.Model):
    receipt_ref = models.ForeignKey(
        SalesReceipt, on_delete=models.CASCADE,
        related_name='returned_items_set', null=True
    )
    sale_item_ref = models.ForeignKey(
        SoldGoods, on_delete=models.CASCADE,
        null=True, blank=True, related_name='sold_items'
    )
    product = models.ForeignKey(
        products.Stock, related_name='returned_stock',
        on_delete=models.CASCADE, null=True    
    )
    unit_of_measurement = models.ForeignKey(
        products.UnitOfMeasurement, on_delete=models.CASCADE,
        null=True
    )
    quantity = models.FloatField(
        verbose_name='Quantity', null=True,
    )
    price = models.FloatField(
        verbose_name='Selling price', null=True
    )
    vat = models.FloatField(
        verbose_name='VAT', default=0
    )
    amount = models.FloatField(
        verbose_name='Amount', default=0
    )

    def __str__(self):
        return '{}'.format(self.receipt_ref)


class SalesInvoice(models.Model):
    invoice_date = models.DateTimeField(
        verbose_name='Date'
    )
    invoice_number = models.CharField(
        verbose_name='Invoice number', max_length=20,
        unique=True
    )
    customer = models.ForeignKey(
        customers.Customer, on_delete=models.CASCADE,
        verbose_name='Credit customer', null=True, blank=True
    )
    salesman = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    total = models.FloatField(
        verbose_name='Total', blank=True, null=True,
        default=0
    )
    slug = models.SlugField(
        default=''
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.invoice_number)
        super(SalesInvoice, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.invoice_number)


class InvoiceGoods (models.Model):
    invoice_ref = models.ForeignKey(
        SalesInvoice, on_delete=models.PROTECT,
        related_name='invoice_items_set'
    )
    product = models.ForeignKey(
        products.Stock, related_name='invoice_stock_item',
        on_delete=models.PROTECT
    )
    unit_of_measurement = models.ForeignKey(
        products.UnitOfMeasurement, on_delete=models.CASCADE,
        null=True
    )
    quantity = models.FloatField(
        verbose_name='Quantity', null=False,
        blank=False
    )
    price = models.FloatField(
        verbose_name='Selling price'
    )
    vat = models.FloatField(
        verbose_name='VAT', default=0
    )
    amount = models.FloatField(
        verbose_name='Amount', default=0
    )
    credit_note = models.BooleanField(
        verbose_name='Void item sale', null=True,
        blank=True
    )


class InvoiceGoodsReturns(models.Model):
    invoice_ref = models.ForeignKey(
        SalesInvoice, on_delete=models.CASCADE,
        related_name='credit_items_set', null=True
    )
    sale_item_ref = models.ForeignKey(
        SoldGoods, on_delete=models.CASCADE,
        null=True, blank=True, related_name='invoice_items'
    )
    product = models.ForeignKey(
        products.Stock, related_name='credit_stock',
        on_delete=models.CASCADE, null=True
    )
    unit_of_measurement = models.ForeignKey(
        products.UnitOfMeasurement, on_delete=models.CASCADE,
        null=True
    )
    quantity = models.FloatField(
        verbose_name='Quantity', null=True,
    )
    price = models.FloatField(
        verbose_name='Selling price', null=True
    )
    vat = models.FloatField(
        verbose_name='VAT', default=0
    )
    amount = models.FloatField(
        verbose_name='Amount', default=0
    )
