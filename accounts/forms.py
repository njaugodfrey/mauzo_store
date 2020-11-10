from django import forms
from .cash_models import CashReceipt, CashReceiptItems
from sales.creditsales import SalesInvoice


class CashReceiptForm(forms.ModelForm):
    class Meta:
        model = CashReceipt
        fields = ['customer', 'description']
        widgets = {
            'customer': forms.Select(attrs={
                'id': 'customer'
            }),
            'description': forms.TextInput
        }


class ReceiptItemsForm(forms.ModelForm):
    class Meta:
        model = CashReceiptItems
        fields = [
            'invoice', 'description', 'amount'
        ]
        widgets = {
            'invoice': forms.Select(attrs={
                'id': 'related_invoice'
            }),
            'description': forms.TextInput(attrs={
                'id': 'receipt_description'
            }),
            'amount': forms.NumberInput(attrs={
                'id': 'receipt_amount'
            })
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['invoice'].queryset = SalesInvoice.objects.none()
