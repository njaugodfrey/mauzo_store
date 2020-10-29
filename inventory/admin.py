from django.contrib import admin
from inventory import models


# Register your models here.

admin.site.register(models.Stock)
admin.site.register(models.GoodsReceipt)
admin.site.register(models.GoodsReturned)
admin.site.register(models.UnitOfMeasurement)
admin.site.register(models.ReceivedGoods)
admin.site.register(models.StockWriteOn)
admin.site.register(models.GoodsWrittenOn)
admin.site.register(models.StockWriteOff)
admin.site.register(models.GoodsWrittenOff)
