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
        if not last_stock:
            obj.stock_code = str(letter_slicer[0:2]) + '0001'
        else:
            stock_code = last_stock.stock_code
            stock_int = int(stock_code[2:6])
            new_stock_int = stock_int + 1
            new_stock_code = str(letter_slicer[0:2]) + str(new_stock_int).zfill(3)
            obj.stock_code = new_stock_code

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


# Goods receipt notes
@login_required
@allowed_user(['Accounts'])
def goods_receipts_list(request):
    context = {}
    context['all_receipts'] = GoodsReceipt.objects.order_by('receipt_number').all()
    return render(
        request, template_name='inventory/goods_receipts_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_goods_receipt(request):
    form = GoodsReceiptForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        last_receipt = GoodsReceipt.objects.all().order_by('receipt_number').last()
        if not last_receipt:
            obj.receipt_number = 'RECEIPT-' + str(1).zfill(4)
        else:
            receipt_number = last_receipt.receipt_number
            receipt_int = int(receipt_number[8:])
            new_receipt_int = receipt_int + 1
            new_receipt_number = 'RECEIPT-' + str(new_receipt_int).zfill(4)
            obj.receipt_number = new_receipt_number
        obj.receipt_date = datetime.today()
        obj.input_by = request.user
        obj.save()
        return redirect(
            'inventory:goods-receipt-detail',
            slug=obj.slug, pk=obj.id
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='inventory/create_goods_receipt.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def goods_receipt_details(request, pk, slug):
    """
    detail view to fill the receipt with items received
    """
    form = ReceivedGoodsForm(request.POST or None)
    receipt = get_object_or_404(
        GoodsReceipt, pk=pk
    )

    context = {
        'form': form,
        'receipt': receipt
    }
    return render(
        request, template_name='inventory/goods_receipt_detail.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def get_units(request):
    stock_id = request.GET.get('item')
    units = UnitOfMeasurement.objects.select_related().filter(stock_id=stock_id)
    return render(
        request, 'inventory/units_list.html',
        {'units': units}
    )


@login_required
@allowed_user(['Accounts'])
def add_receipt_items(request, pk, slug):
    if request.method == 'POST':
        # grab form values
        item = request.POST.get('item')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        unit = request.POST.get('unit')
        response_data = {}

        # process the form
        receipt_item = ReceivedGoods(
            document_ref=GoodsReceipt.objects.get(id=pk),
            stock=Stock.objects.get(pk=item),
            quantity=quantity,
            unit_of_measurement= UnitOfMeasurement.objects.get(pk=unit),
            price=price,
            amount=int(quantity)*int(price)
        )
        receipt_item.save()

        # update unit prices
        item_unit = UnitOfMeasurement.objects.get(pk=unit)
        item_unit.purchase_price = price
        item_unit.save()

        # update the stock quantity
        stock_item = Stock.objects.get(pk=item)
        received_stock = float(item_unit.base_quantity) * float(quantity)
        stock_item.quantity = stock_item.quantity + received_stock
        stock_item.save()

        # update total
        receipt_total = GoodsReceipt.objects.get(id=pk)
        receipt_total.total = receipt_total.total  + (int(quantity)*int(price))
        receipt_total.save()

        # data to respond with
        response_data['result'] = 'Item saved successfully'
        response_data['item_id'] = receipt_item.pk
        response_data['item_name'] = receipt_item.stock.stock_name
        response_data['item_quantity'] = receipt_item.quantity
        response_data['item_price'] = receipt_item.price
        response_data['total_cost'] = receipt_item.amount

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "action not successful"}),
            content_type="application/json"
        )


@login_required
@allowed_user(['Accounts'])
@csrf_exempt
def remove_receipt_items(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = ReceivedGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_stock = item.stock
        item.delete()
        stock_obj = Stock.objects.get(pk=item_stock.pk)
        stock_obj_quantity = stock_obj.quantity
        stock_obj.quantity = int(stock_obj_quantity) - int(item.quantity)
        stock_obj.save()

        response_data = {}
        response_data['msg'] = 'Item removed.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
@allowed_user(['Accounts'])
def print_grn(request, pk):
    receipt = GoodsReceipt.objects.get(pk=pk)
    items = ReceivedGoods.objects.filter(document_ref=pk).select_related()
    fieldnames = ['Code', 'Item', 'Unit']
    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="grn.txt"'
    head = csv.writer(response)
    body = csv.DictWriter(response, fieldnames=fieldnames)
    head.writerow(['Gathee Wholesalers'])
    body.writeheader()
    for item in items:
        body.writerow({
            'Code': item.stock.stock_code,
            'Item': item.stock.stock_name,
            'Unit': item.unit_of_measurement.unit_name
        })
    

    return response


# Goods returns notes
@login_required
@allowed_user(['Accounts'])
def goods_returns_list(request):
    context = {}
    context['all_returns'] = GoodsReturned.objects.all()
    return render(
        request, template_name='inventory/goods_returns_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_returns(request):
    form = GoodsReturnsForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        last_return = GoodsReturned.objects.all().order_by('return_number').last()
        if not last_return:
            obj.return_number = 'RETURN-' + str(1).zfill(4)
        else:
            return_number = last_return.return_number
            return_int = int(return_number[6:11])
            new_return_int = return_int + 1
            new_return_number = 'RETURN-' + str(new_return_int).zfill(4)
            obj.return_number = new_return_number
        obj.return_date = datetime.today()
        obj.input_by = request.user
        obj.save()
        return redirect(
            'inventory:goods-returns-detail',
            slug=obj.slug, pk=obj.id
        )
    
    context = {
        'form': form
    }
    return render(
        request, template_name='inventory/create_goods_returns.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def goods_returns_detail(request, pk, slug):
    returns = get_object_or_404(GoodsReturned, pk=pk)
    items = ReturnedGoods.objects.filter(document_ref=pk).select_related()
    form = ReturnedGoodsForm(request.POST or None)
    context = {
        'return': returns,
        'items': items,
        'form': form
    }
    return render(
        request, template_name='inventory/goods_returned_detail.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def add_returns_items(request, pk, slug):
    if request.method == 'POST':
        # grab from values
        item = request.POST.get('item')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        unit = request.POST.get('unit')
        response_data = {}

        # process the form
        return_item = ReturnedGoods(
            document_ref=GoodsReceipt.objects.get(id=pk),
            stock=Stock.objects.get(pk=item),
            quantity=quantity,
            price=price,
            amount=int(quantity)*int(price)
        )
        return_item.save()

        # update the stock quantity
        item_unit = UnitOfMeasurement.objects.get(pk=unit)
        stock_item = Stock.objects.get(pk=item)
        returned_stock = float(item_unit.base_quantity) * float(quantity)
        stock_item.quantity = stock_item.quantity - returned_stock
        stock_item.save()

        # data to respond with
        response_data['result'] = 'Item saved successfully'
        response_data['item_id'] = return_item.pk
        response_data['item_name'] = return_item.stock.stock_name
        response_data['item_quantity'] = return_item.quantity
        response_data['item_price'] = return_item.price
        response_data['total_cost'] = return_item.amount

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "action not successful"}),
            content_type="application/json"
        )


@login_required
@allowed_user(['Accounts'])
@csrf_exempt
def remove_returns_items(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = ReturnedGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_stock = item.stock
        item.delete()
        stock_obj = Stock.objects.get(pk=item_stock.pk)
        stock_obj_quantity = stock_obj.quantity
        stock_obj.quantity = int(stock_obj_quantity) + int(item.quantity)
        stock_obj.save()

        response_data = {'msg': 'Item removed.'}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


# writeons
@login_required
@allowed_user(['Accounts'])
def create_write_on(request):
    last_write_on = StockWriteOn.objects.all().order_by('write_on_number').last()
    if not last_write_on:
        write_on_number = 'SWO-' + str(1).zfill(4)
    else:
        document_number = last_write_on.write_on_number
        document_int = int(document_number[4:])
        new_document_int = document_int + 1
        new_document_number = 'SWO-' + str(new_document_int).zfill(4)
        write_on_number = new_document_number
    write_on_date = datetime.today()
    input_by = request.user

    new_write_on = StockWriteOn(
        write_on_date=write_on_date,
        write_on_number=write_on_number,
        input_by=input_by
    )
    new_write_on.save()
    return redirect(
        'inventory:writeon-detail',
        slug=new_write_on.slug, pk=new_write_on.pk
    )


@login_required
def write_on_list(request):
    context = {
        'writeons': StockWriteOn.objects.order_by('write_on_date').all()
    }
    return render(
        request, template_name='inventory/write_on_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def write_on_detail(request, pk, slug):
    form = WriteOnForm(request.POST or None)
    writeon = get_object_or_404(StockWriteOn, pk=pk)
    items = GoodsWrittenOn.objects.filter(document_ref=writeon.id).select_related()

    context = {
        'form': form,
        'writeon': writeon,
        'items': items
    }
    return render(
        request, template_name='inventory/stock_write_on.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def add_write_on_items(request, pk, slug):
    if request.method == 'POST':
        item = request.POST.get('item')
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')

        # process form
        write_on_item = GoodsWrittenOn(
            document_ref=StockWriteOn.objects.get(id=pk),
            stock=Stock.objects.get(pk=item),
            quantity=quantity,
            unit_of_measurement=UnitOfMeasurement.objects.get(pk=unit)
        )
        write_on_item.save()

        # update stock quantity
        item_unit = UnitOfMeasurement.objects.get(pk=unit)
        stock_item = Stock.objects.get(pk=item)
        received_stock = float(item_unit.base_quantity) * float(quantity)
        stock_item.quantity = stock_item.quantity + received_stock
        stock_item.save()

        # data to respond with
        response_data = {
            'result': 'Item saved successfully',
            'item_id': write_on_item.pk,
            'item_name': write_on_item.stock.stock_name,
            'itme_quantity': write_on_item.quantity
        }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "action not successful"}),
            content_type="application/json"
        )

@login_required
@csrf_exempt
def remove_writeon_item(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = ReceivedGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_stock = item.stock
        item.delete()
        stock_obj = Stock.objects.get(pk=item_stock.pk)
        stock_obj_quantity = stock_obj.quantity
        stock_obj.quantity = int(stock_obj_quantity) - int(item.quantity)
        stock_obj.save()

        response_data = {}
        response_data['msg'] = 'Item removed.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

