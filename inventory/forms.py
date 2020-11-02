from django import forms
from inventory import models


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = models.Stock
        fields = [
            'stock_name', 'stock_supplier', 'quantity',
            'stock_vat_code', 'unit_quantity'
        ]


class UnitCreateForm(forms.ModelForm):
    class Meta:
        model = models.UnitOfMeasurement
        fields = [
            'unit_name', 'unit_description', 'base_quantity',
            'stock', 'purchase_price', 'selling_price'
        ]


class GoodsReceiptForm(forms.ModelForm):
    class Meta:
        model = models.GoodsReceipt
        fields = ['supplier']


class GoodsReturnsForm(forms.ModelForm):
    class Meta:
        model = models.GoodsReturned
        fields = ['supplier']


class ReceivedGoodsForm(forms.ModelForm):
    class Meta:
        model = models.ReceivedGoods
        fields = [
            'stock', 'quantity', 'unit_of_measurement', 'price'
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'id': 'item-quantity', 
                'required': True, 
                'placeholder': 'Quantity...'
            }),
            'stock': forms.Select(attrs={
                'id': 'item-name',
                'required': True
            }),
            'price': forms.NumberInput(attrs={
                'id': 'item-price',
                'required': True
            }),
            'unit_of_measurement': forms.Select(attrs={
                'id': 'uom',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit_of_measurement'].queryset = models.UnitOfMeasurement.objects.none()


class ReturnedGoodsForm(forms.ModelForm):
    class Meta:
        model = models.ReturnedGoods
        fields = [
            'stock', 'quantity', 'unit_of_measurement', 'price'
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'id': 'item-quantity', 
                'required': True, 
                'placeholder': 'Quantity...'
            }),
            'stock': forms.Select(attrs={
                'id': 'item-name',
                'required': True
            }),
            'price': forms.NumberInput(attrs={
                'id': 'item-price',
                'required': True
            }),
            'unit_of_measurement': forms.Select(attrs={
                'id': 'uom',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit_of_measurement'].queryset = models.UnitOfMeasurement.objects.none()


class WriteOnForm(forms.ModelForm):
    class Meta:
        model = models.GoodsWrittenOn
        fields = [
            'stock', 'quantity', 'unit_of_measurement'
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'id': 'item-quantity',
                'required': True,
                'placeholder': 'Quantity...'
            }),
            'stock': forms.Select(attrs={
                'id': 'item-name',
                'required': True
            }),
            'unit_of_measurement': forms.Select(attrs={
                'id': 'uom',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit_of_measurement'].queryset = models.UnitOfMeasurement.objects.none()


class WriteOffForm(forms.ModelForm):
    class Meta:
        model = models.GoodsWrittenOff
        fields = [
            'stock', 'quantity', 'unit_of_measurement'
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'id': 'item-quantity',
                'required': True,
                'placeholder': 'Quantity...'
            }),
            'stock': forms.Select(attrs={
                'id': 'item-name',
                'required': True
            }),
            'unit_of_measurement': forms.Select(attrs={
                'id': 'uom',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit_of_measurement'].queryset = models.UnitOfMeasurement.objects.none()
