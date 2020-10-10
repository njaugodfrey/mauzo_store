from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_name', 'customer_full_name',
            'phone_number', 'location', 'opening_balance'
        ]
