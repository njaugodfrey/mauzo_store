import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.http import HttpResponse, QueryDict
from django.db.models import Sum

from .forms import CashReceiptForm, ReceiptItemsForm
from .cash_models import CashReceipt, CashReceiptItems
from customer.models import Customer


def cash_receipts_list(request):
    context = {
        'all_receipts': CashReceipt.objects.all().order_by('receipt_date')
    }
    return render(
        request, template_name='accounts/cash_receipts_list.html',
        context=context
    )


def receipt_via_customer(request, pk):
    last_receipt = CashReceipt.objects.all().order_by('receipt_number').last()
    if not last_receipt:
        receipt_number = '1'.zfill(6)
    else:
        receipt_number = str(int(last_receipt.receipt_number) + 1).zfill(6)
    
    new_receipt = CashReceipt(
        customer=get_object_or_404(Customer, pk=pk),
        receipt_date=datetime.today(),
        receipt_number=receipt_number,
        description='',
        user=request.user,
        total=0
    )
    new_receipt.save()
    return redirect(
        'accounts:cash-receipt-detail',
        slug=new_receipt.slug, pk=new_receipt.pk
    )


def create_cash_receipt(request):
    form = CashReceiptForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            obj = form.save(commit=False)
            last_receipt = CashReceipt.objects.all().order_by('receipt_number').last()
            if not last_receipt:
                obj.receipt_number = '1'.zfill(6)
            else:
                obj.receipt_number = str(int(last_receipt.receipt_number) + 1).zfill(6)
            
            obj.receipt_date = datetime.today()
            obj.user = request.user
            obj.total = 0
            obj.save()
            return redirect(
                'accounts:cash-receipt-detail', slug = obj.slug, pk=obj.id
            )
    
    context = {'form': form}
    return render(
        request, template_name='accounts/create_cash_receipt.html',
        context=context
    )


def view_cash_receipt(request, pk, slug):
    receipt = get_object_or_404(CashReceipt, pk=pk)
    form = ReceiptItemsForm(request.POST or None)
    
    context = {
        'receipt': receipt,
        'form': form
    }
    return render(
        request, template_name='accounts/view_cash_receipt.html',
        context=context
    )
