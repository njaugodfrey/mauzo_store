from django.contrib import admin
from .models import vat
from .cash_models import *

# Register your models here.

admin.site.register (vat)
admin.site.register(CashReceipt)
admin.site.register(CashReceiptItems)
