from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from mauzo.decorators import allowed_user
from .models import Customer
from .forms import CustomerForm
from sales.models import SalesReceipt


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
    invoices = SalesReceipt.objects.filter(
        debtors_account=customer.customer_code
    ).select_related()
    context = {
        'customer': customer,
        'invoices': invoices
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
        all_customers = Customer.objects.all()
        customer_code = str(obj.customer_name[0:1]) + '001'
        if customer_code in all_customers:
            customer_int = int(customer_code[1:4])
            new_customer_int = customer_int + 1
            new_customer_code = str(obj.customer_name[0:1]) + str(new_customer_int).zfill(3)
            obj.customer_code = new_customer_code
        else:
            obj.customer_code = customer_code
        
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
