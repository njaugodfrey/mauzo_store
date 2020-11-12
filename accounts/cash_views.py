import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.http import HttpResponse, QueryDict
from django.db.models import Sum

from .forms import CashReceiptForm, ReceiptItemsForm
from .cash_models import CashReceipt, CashReceiptItems
from customer.models import Customer
from sales.models import SalesInvoice


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
    details = CashReceiptItems.objects.filter(receipt_ref=receipt.id).select_related()
    
    context = {
        'receipt': receipt,
        'form': form,
        'details': details
    }
    return render(
        request, template_name='accounts/view_cash_receipt.html',
        context=context
    )


def filter_invoices(request):
    customer_id = request.GET.get('customer')
    invoices = SalesInvoice.objects.filter(customer=customer_id).select_related()
    return render(
        request, template_name='accounts/rcpt_invoices_list.html',
        context={'invoices': invoices}
    )


def add_receipt_items(request, pk, slug):
    if request.method == 'POST':
        invoice = request.POST.get('invoice')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if invoice is '\'\'':
            invoice = None
        else:
            invoice = SalesInvoice.objects.get(id=invoice)

        receipt_item = CashReceiptItems(
            receipt_ref=CashReceipt.objects.get(id=pk),
            invoice=invoice,
            description=description,
            amount=amount
        )
        receipt_item.save()

        receipt_total = receipt_item.receipt_ref.total + amount
        receipt_total.save()

        response_data = {
            'result': 'Item saved successfully',
            'invoice': receipt_item.invoice,
            'description': receipt_item.description,
            'amount': receipt_item.amount
        }

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )

    else:
        return HttpResposne(
            json.dumps({
                'error': 'input unsuccessful'
            }),
            content_type='application/json'
        )
