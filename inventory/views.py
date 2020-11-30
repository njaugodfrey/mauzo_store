from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, QueryDict
from django.utils.timezone import datetime
from django.contrib.auth.decorators import login_required

import json, csv

from .models import *
from .forms import *
from mauzo.decorators import allowed_user


# Create your views here.
# views for grn and stock take in respective .py files

# Inventory stocks
@login_required
@allowed_user(['Accounts'])
def stocks_list(request):
    context = {}
    context['all_items'] = Stock.objects.order_by('stock_code').all()
    return render(
        request, template_name='inventory/inventory_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def stock_detail(request, pk, slug):
    item = Stock.objects.get(pk=pk)
    received = ReceivedGoods.objects.filter(
        stock=pk
    ).order_by(
        '-document_ref__receipt_date'
    ).select_related()
    units = UnitOfMeasurement.objects.filter(
        stock=pk
    ).select_related()
    context = {
        'item': item,
        'units': units,
        'received_items': received
    }
    return render(
        request, 'inventory/item_detail.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_stock(request):
    form = StockCreateForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        # stock code generator
        last_stock = Stock.objects.all().order_by('stock_code').last()
        letter_slicer = obj.stock_name
        '''if not last_stock:
            obj.stock_code = str(letter_slicer[0:1]) + '0001'
        else:
            stock_code = last_stock.stock_code
            stock_int = int(stock_code[2:6])
            new_stock_int = stock_int + 1
            new_stock_code = str(letter_slicer[0:1]) + str(new_stock_int).zfill(4)
            obj.stock_code = new_stock_code'''

        if not last_stock:
            obj.stock_code = '1'.zfill(4)
        else:
            obj.stock_code = str(int(last_stock.stock_code) + 1).zfill(4)

        #obj.stock_code = random.randint(1000, 9999)
        obj.save()
        return redirect(
            'inventory:stock_detail',
            slug=obj.slug, pk=obj.id
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='inventory/stock_form.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def update_stock(request, pk, slug):
    stock = get_object_or_404(Stock, pk=pk)
    form = StockCreateForm(
        request.POST or None, instance=stock
    )

    if form.is_valid():
        form.save()
        return redirect(
            'inventory:stock_detail',
            slug=stock.slug, pk=stock.id
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='inventory/stock_form.html',
        context=context
    )


# Units of measurement
@login_required
@allowed_user(['Accounts'])
def units_list(request):
    context = {}
    context['all_units'] = UnitOfMeasurement.objects.all()
    return render(
        request, template_name='inventory/uom_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def unit_detail(request, pk):
    uom = get_object_or_404(UnitOfMeasurement, pk=pk)
    context = {
        'uom': uom
    }
    return render(
        request, template_name='inventory/uom_detail.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_unit(request):
    form = UnitCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(
            'inventory:stock_detail',
            pk=form.instance.stock.id,
            slug=form.instance.stock.slug
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='inventory/unitofmeasurement_form.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def update_unit(request, pk):
    uom = get_object_or_404(UnitOfMeasurement, pk=pk)
    form = UnitCreateForm(
        request.POST or None, instance=uom
    )
    
    if form.is_valid():
        form.save()
        return redirect(
            'inventory:stock_detail',
            pk=form.instance.stock.id,
            slug=form.instance.stock.slug
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='inventory/unitofmeasurement_form.html',
        context=context
    )


@login_required
def get_units(request):
    stock_id = request.GET.get('item')
    units = UnitOfMeasurement.objects.select_related().filter(stock_id=stock_id)
    return render(
        request, 'inventory/units_list.html',
        {'units': units}
    )
