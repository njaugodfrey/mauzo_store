from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import generic

from mauzo.decorators import allowed_user
from .models import Supplier
from .forms import SupplierForm
from inventory.models import GoodsReceipt, GoodsReturned

# Create your views here.


@login_required
@allowed_user(['Accounts'])
def suppliers_list(request):
    context = {}
    context['all_suppliers'] = Supplier.objects.all()
    return render(
        request, 'supplier/suppliers_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def supplier_detail(request, pk, slug):
    supplier = Supplier.objects.get(supplier_code=pk)
    goods_receipts = GoodsReceipt.objects.filter(supplier=pk).all()
    goods_returns = GoodsReturned.objects.filter(supplier=pk)
    context = {
        'supplier': supplier,
        'receipts': goods_receipts,
        'returns': goods_returns
    }
    return render(
        request, template_name='supplier/supplier_detail.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_supplier(request):
    form = SupplierForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        
        # auto assign supplier code
        all_suppliers = Supplier.objects.all()
        supplier_code = str(obj.supplier_name[0:1]) + '001'
        if supplier_code in all_suppliers:
            supplier_int = int(supplier_code[1:4])
            new_supplier_int = supplier_int + 1
            new_supplier_code = str(obj.supplier_name[0:1]) + str(new_supplier_int).zfill(3)
            obj.supplier_code = new_supplier_code
        else:
            obj.supplier_code = supplier_code
        
        obj.save()
        return redirect(
            'supplier:supplier_detail',
            pk=obj.supplier_code, slug=obj.slug
        )

    context = {
        'form': form
    }
    return render(
        request, template_name='supplier/create_supplier.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def update_supplier(request, pk, slug):
    supplier = get_object_or_404(Supplier, supplier_code=pk)
    form = SupplierForm(
        request.POST or None, instance=supplier
    )
    
    if form.is_valid():
        form.save
        return redirect(
            'supplier:supplier_detail',
            pk=supplier.supplier_code, slug=supplier.slug
        )
    
    context = {
        'form': form
    }    
    return render(
        request, template_name='supplier/create_supplier.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, supplier_code=pk)

    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier:all_suppliers')
    
    context = {'supplier': supplier}
    return render(
        request, template_name='supplier/delete_supplier.html',
        context=context
    )
