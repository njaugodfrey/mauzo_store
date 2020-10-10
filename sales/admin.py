from django.contrib import admin
from sales import models

# Register your models here.

admin.site.register(models.SalesReceipt)
admin.site.register(models.SoldGoods)
admin.site.register(models.SalesReceiptVoid)
