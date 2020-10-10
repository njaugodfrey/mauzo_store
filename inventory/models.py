from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from supplier.models import Supplier
from accounts.models import vat


# Create your models here.


class Stock(models.Model):
    stock_code = models.CharField(
        verbose_name='Stock code',
        unique=True, null=False, max_length=20
    )
    stock_name = models.CharField(
        verbose_name='Name', null=False,
        blank=False, max_length=100
    )
    unit_quantity = models.IntegerField(
        verbose_name='Base unit quantity', default=1,
        help_text='Minimum amount of quantity in an item'
    )
    unit_name = models.CharField(
        verbose_name='Unit name', default='unit',
        max_length=10
    )
    stock_supplier = models.ManyToManyField(
        Supplier
    )
    purchase_price = models.FloatField(
        verbose_name='Purchase price'
    )
    selling_price_1 = models.FloatField(
        verbose_name='Selling price 1'
    )
    selling_price_2 = models.FloatField(
        verbose_name='Selling price 2'
    )
    quantity = models.FloatField(
        verbose_name='Stock in hand', default=0
    )
    stock_vat_code = models.ForeignKey(
        vat, on_delete=models.PROTECT
    )
    sales_discount = models.IntegerField(
        null=True, blank=True
    )
    is_promotional = models.BooleanField(
        default=False
    )
    slug = models.SlugField(
        default=''
    )

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return '{}'.format(self.stock_name)
    
    '''def stock_calculator(self):
        sales = SalesReceipt.objects.'''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.stock_name)
        super(Stock, self).save(*args, **kwargs)


class UnitOfMeasurement(models.Model):
    unit_name = models.CharField(
        verbose_name='Unit name', max_length=50,
    )
    unit_description = models.TextField(
        verbose_name='Description', null=True, blank=True
    )
    base_quantity = models.FloatField(
        verbose_name='Minimum quantity'
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.PROTECT
    )
    purchase_price = models.FloatField(
        verbose_name='Buying price', default=0
    )
    selling_price = models.FloatField(
        verbose_name='Selling price', default=0
    )
    slug = models.SlugField(
        default=''
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.unit_name)
        super(UnitOfMeasurement, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.unit_name)


class GoodsReceipt(models.Model):
    receipt_date = models.DateTimeField(
        verbose_name='Date', auto_now_add=True
    )
    receipt_number = models.CharField(
        verbose_name='Reference', null=False,
        max_length=50
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE,
        null=True
    )
    input_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Input by: '
    )
    total = models.FloatField(
        default=0
    )
    slug = models.SlugField(
        default=''
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.receipt_number)
        super(GoodsReceipt, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{}'.format(self.receipt_number)


class GoodsReturned(models.Model):
    return_date = models.DateTimeField(
        verbose_name='Date', auto_now_add=True
    )
    return_number = models.CharField(
        verbose_name='Reference', null=False,
        max_length=50
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE,
        null=True
    )
    input_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Input by: '
    )
    total = models.FloatField(default=0)
    slug = models.SlugField(
        default=''
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.return_number)
        super(GoodsReturned, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{}'.format(self.return_number)
    

class ReceivedGoods(models.Model):
    document_ref = models.ForeignKey(
        GoodsReceipt, on_delete=models.PROTECT,
        related_name='receipt_note'
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.PROTECT
    )
    quantity = models.IntegerField(
        verbose_name='Quantity'
    )
    unit_of_measurement = models.ForeignKey(
        UnitOfMeasurement,
        on_delete=models.SET_NULL, null=True
    )
    price = models.FloatField(
        verbose_name='Buying price'
    )
    amount = models.FloatField(
        verbose_name='Amount'
    )


class ReturnedGoods(models.Model):
    document_ref = models.ForeignKey(
        GoodsReceipt, on_delete=models.PROTECT
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.PROTECT
    )
    quantity = models.IntegerField(
        verbose_name='Quantity'
    )
    unit_of_measurement = models.ForeignKey(
        UnitOfMeasurement,
        on_delete=models.SET_NULL, null=True
    )
    price = models.FloatField(
        verbose_name='Buying price'
    )
    amount = models.FloatField(
        verbose_name='Amount'
    )

