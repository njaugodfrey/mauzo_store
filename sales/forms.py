from django import forms
from .models import *
from inventory import models as inventory


class SalesReceiptForm(forms.ModelForm):
    class Meta:
        model = SalesReceipt
        fields = [
            'walkin_customer', 'debtors_account'
        ]


class SoldGoodsForm(forms.ModelForm):
    class Meta:
        model = SoldGoods
        fields = [
            'product', 'quantity', 'unit_of_measurement'
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'id': 'item-quantity', 
                'required': True, 
                'placeholder': 'Quantity...'
            }),
            'product': forms.Select(attrs={
                'id': 'item-name',
                'required': True
            }),
            'unit_of_measurement': forms.Select(attrs={
                'id': 'uom',
                'required': True,
                'value': 0
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit_of_measurement'].queryset = inventory.UnitOfMeasurement.objects.none()
