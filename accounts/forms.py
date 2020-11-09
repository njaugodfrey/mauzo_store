from django import forms
from .cash_models import CashReceipt, CashReceiptItems
from sales.creditsales import SalesInvoice


class CashReceiptForm(forms.ModelForm):
    class Meta:
        model = CashReceipt
        fields = ['customer', 'description']


class ReceiptItemsForm(forms.ModelForm):
    class Meta:
        model = CashReceiptItems
        fields = [
            'invoice', 'description', 'amount'
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['invoice'].queryset = SalesInvoice.objects.none()
