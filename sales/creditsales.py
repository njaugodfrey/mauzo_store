import json

from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.db.models import Sum

from .forms import SoldGoodsForm
from .models import SalesInvoice, InvoiceGoodsReturns, InvoiceGoods
from inventory.models import Stock, UnitOfMeasurement
from accounts.cash_model import CashReceipt
from customer.models import Customer
from companyprofile.models import Company
from mauzo.decorators import allowed_user


@login_required
@allowed_user(['Accounts'])
def invoices_list(request):
    context = {'invoices': SalesInvoice.objects.all()}
    return render(
        request, template_name='',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_sales_invoice(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    last_invoice = SalesInvoice.objects.all().order_by('invoice_number').last()
    if not last_invoice:
        invoice_number = 'SI' + str(datetime.today().month).zfill(2) + \
                         str(datetime.today().day).zfill(2) + '001'
    else:
        invoice_number = last_invoice.receipt_number
        invoice_int = int(invoice_number[7:11])
        new_invoice_int = invoice_int + 1
        new_invoice_number = 'SI' + str(datetime.today().month).zfill(2) + \
                             str(datetime.today().day).zfill(2) + str(new_invoice_int).zfill(4)
        invoice_number = new_invoice_number
    sale_date = datetime.today()
    salesman = request.user

    new_invoice = SalesInvoice(
        sale_date=sale_date,
        receipt_number=invoice_number,
        customer=customer,
        salesman=salesman
    )
    new_invoice.save()
    return redirect(
        '', slug=new_invoice.slug, pk=new_invoice.id
    )


@login_required
@allowed_user(['Accounts'])
def sales_invoice_detail(request, pk, slug):
    invoice = get_object_or_404(SalesInvoice, pk=pk)
    form = SoldGoodsForm(request.POST or None)
    items = InvoiceGoods.objects.filter(invoice_ref=invoice.id).select_related()

    context = {
        'invoice': invoice,
        'items': items,
        'form': form
    }
    return render(
        request, template_name='',
        context=context
    )
