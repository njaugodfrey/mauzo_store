from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from mauzo.decorators import allowed_user
from .models import Customer
from .forms import CustomerForm
from sales.creditsales import SalesInvoice, InvoiceGoodsReturns
from accounts.cash_models import CashReceipt


# Create your views here.


@login_required
@allowed_user(['Accounts'])
def customers_list(request):
    context = {
        'all_customers': Customer.objects.order_by('customer_code').all()
    }
    return render(
        request, template_name='customer/customers_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def customer_detail(request, pk, slug):
    customer = Customer.objects.get(customer_code=pk)
    invoices = SalesInvoice.objects.filter(
        customer=pk
    ).select_related()
    payments = CashReceipt.objects.filter(
        customer=pk
    ).select_related()
    context = {
        'customer': customer,
        'invoices': invoices,
        'payments': payments
    }
    return render(
        request, template_name='customer/customer_detail.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_customer(request):
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        
        # auto assign customer code
        last_customer = Customer.objects.all().order_by('customer_code').last()
        customer_code = str(obj.customer_name[0:1]) + '001'
        if not last_customer:
            obj.customer_code = customer_code
        else:
            customer_int = int(customer_code[1:])
            new_customer_int = customer_int + 1
            new_customer_code = str(obj.customer_name[0:1]) + str(new_customer_int).zfill(3)
            obj.customer_code = new_customer_code
        
        obj.save()
        return redirect(
            'customer:customer_detail',
            pk=obj.customer_code, slug=obj.slug
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='customer/create_customer.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def update_supplier(request, pk, slug):
    customer = get_object_or_404(Customer, customer_code=pk)
    form = CustomerForm(
        request.POST or None, instance=customer
    )

    if form.is_valid():
        form.save()
        return redirect(
            'customer:customer_detail',
            pk=customer.customer_code, slug=customer.slug
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='customer/create_customer.html',
        context=context
    )
