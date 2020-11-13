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

        if invoice == '':
            receipt_item = CashReceiptItems(
            receipt_ref=CashReceipt.objects.get(id=pk),
            description=description,
            amount=amount
        )
        else:
            receipt_item = CashReceiptItems(
            receipt_ref=CashReceipt.objects.get(id=pk),
            invoice=SalesInvoice.objects.get(id=invoice),
            description=description,
            amount=amount
        )
        receipt_item.save()

        receipt_item.receipt_ref.total = float(receipt_item.receipt_ref.total) + float(amount)
        receipt_item.receipt_ref.save()

        response_data = {}
        response_data['result'] = 'Item saved successfully'
        if receipt_item.invoice is None:
            response_data['invoice'] = 'None'
        else:
            response_data['invoice'] = receipt_item.invoice.invoice_number

        response_data['description'] = receipt_item.description
        response_data['amount'] = receipt_item.amount

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


def cancel_receipt_item(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = CashReceiptItems.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        related_receipt = item.receipt_ref
        item_amount = item.amount
        item.delete()

        receipt_obj = CashReceipt.objects.get(pk=related_receipt.pk)
        receipt_obj.total = float(receipt_obj.total) - float(item_amount)
        receipt_obj.save()

        response_data = {
            'msg': 'item removed',
            'receipt_total': receipt_obj.total
        }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
