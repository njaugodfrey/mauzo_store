from django.contrib import admin
from sales import models

# Register your models here.

admin.site.register(models.SalesReceipt)
admin.site.register(models.SoldGoods)
admin.site.register(models.SalesReceiptVoid)
admin.site.register(models.SalesInvoice)
admin.site.register(models.InvoiceGoodsReturns)
