import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.utils.timezone import datetime
from django.contrib.auth.decorators import login_required

from .models import (
    GoodsReceipt, ReceivedGoods,
    GoodsReturned, ReturnedGoods,
    Stock, UnitOfMeasurement,
    StockCardEntry
)
from .forms import (
    GoodsReceiptForm, GoodsReturnsForm,
    ReceivedGoodsForm, ReturnedGoodsForm
)
from mauzo.decorators import allowed_user

# Goods receipt notes
@login_required
@allowed_user(['Accounts'])
def goods_receipts_list(request):
    context = {
        'all_receipts': GoodsReceipt.objects.order_by('receipt_number').all()
    }
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
    items = ReceivedGoods.objects.filter(document_ref=receipt.id).select_related()

    context = {
        'form': form,
        'receipt': receipt,
        'items': items
    }
    return render(
        request, template_name='inventory/goods_receipt_detail.html',
        context=context
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
            unit_of_measurement=UnitOfMeasurement.objects.get(pk=unit),
            price=price,
            amount=float(quantity) * float(price)
        )
        receipt_item.save()

        # update unit prices
        item_unit = UnitOfMeasurement.objects.get(pk=unit)
        """item_unit.purchase_price = price
        item_unit.save()"""

        # update the stock quantity
        stock_item = Stock.objects.get(pk=item)
        received_stock = float(item_unit.base_quantity) * float(quantity)
        stock_item.quantity = stock_item.quantity + received_stock
        stock_item.save()

        # update receipt total
        receipt_total = GoodsReceipt.objects.get(id=pk)
        receipt_total.total = receipt_total.total  + (float(quantity) * float(price))
        receipt_total.save()

        # log in stock card
        stock_card = StockCardEntry(
            stock=Stock.objects.get(pk=item),
            document=GoodsReceipt.objects.get(id=pk).receipt_number,
            quantity=float(quantity) * float(item_unit.base_quantity),
            unit=item_unit,
            price=price,
            amount=float(quantity) * float(item_unit.base_quantity) * float(price)
        )
        stock_card.save()
        receipt_item.log_number = stock_card.pk
        receipt_item.save()

        # data to respond with
        response_data['result'] = 'Item saved successfully'
        response_data['item_id'] = receipt_item.pk
        response_data['item_name'] = receipt_item.stock.stock_name
        response_data['item_quantity'] = receipt_item.quantity
        response_data['item_price'] = receipt_item.price
        response_data['total_cost'] = receipt_item.amount
        response_data['document_total'] = receipt_total.total

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
def remove_receipt_items(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = ReceivedGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_stock = item.stock
        item_unit = item.unit_of_measurement
        item_total = item.amount
        receipt = item.document_ref
        entry = StockCardEntry.objects.get(pk=item.log_number)
        entry.delete()
        item.delete()

        # update stock quantity
        stock_obj = Stock.objects.get(pk=item_stock.pk)
        stock_obj_quantity = stock_obj.quantity
        remove_quantity = float(item_unit.base_quantity) * float(item.quantity)
        stock_obj.quantity = float(stock_obj_quantity) - float(remove_quantity)
        stock_obj.save()

        # update receipt value
        receipt_obj = GoodsReceipt.objects.get(pk=receipt.pk)
        item_amount = float(item.quantity) * float(item_unit.purchase_price)
        receipt_obj.total = receipt_obj.total - item_amount
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


# Goods returns notes
@login_required
@allowed_user(['Accounts'])
def goods_returns_list(request):
    context = {
        'all_returns': GoodsReturned.objects.all()
    }
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
        unit = request.POST.get('unit')
        response_data = {}

        unit_obj =  UnitOfMeasurement.objects.get(pk=unit)
        unit_price = unit_obj.purchase_price

        # process the form
        return_item = ReturnedGoods(
            document_ref=GoodsReturned.objects.get(id=pk),
            stock=Stock.objects.get(pk=item),
            quantity=quantity,
            unit_of_measurement= unit_obj,
            price=unit_price,
            amount=float(quantity) * float(unit_price)
        )
        return_item.save()

        # update the stock quantity
        item_unit = UnitOfMeasurement.objects.get(pk=unit)
        stock_item = Stock.objects.get(pk=item)
        returned_stock = float(item_unit.base_quantity) * float(quantity)
        stock_item.quantity = stock_item.quantity - returned_stock
        stock_item.save()

        # log in stock card
        stock_card = StockCardEntry(
            stock=Stock.objects.get(pk=item),
            document=GoodsReturned.objects.get(id=pk).return_number,
            quantity=-(float(quantity) * float(item_unit.base_quantity)),
            unit=item_unit,
            price=-unit_price,
            amount=-float(quantity) * float(item_unit.base_quantity) * float(unit_price)
        )
        stock_card.save()
        return_item.log_number = stock_card.pk
        return_item.save()

        # update returns total
        return_total = GoodsReturned.objects.get(id=pk)
        return_total.total = return_total.total + (float(quantity) * float(unit_price))
        return_total.save()

        # data to respond with
        response_data['result'] = 'Item saved successfully'
        response_data['item_id'] = return_item.pk
        response_data['item_name'] = return_item.stock.stock_name
        response_data['item_quantity'] = return_item.quantity
        response_data['item_price'] = return_item.price
        response_data['total_cost'] = return_item.amount
        response_data['document_total'] = return_total.total

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
def remove_returns_items(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = ReturnedGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_stock = item.stock
        item_unit = item.unit_of_measurement
        entry = StockCardEntry.objects.get(pk=item.log_number)
        entry.delete()
        item_total = item.amount
        receipt = item.document_ref
        item.delete()

        # update stock quantity
        stock_obj = Stock.objects.get(pk=item_stock.pk)
        stock_obj_quantity = stock_obj.quantity
        remove_quantity = float(item_unit.base_quantity) * float(item.quantity)
        stock_obj.quantity = float(stock_obj_quantity) + float(remove_quantity)
        stock_obj.save()

        # update receipt value
        receipt_obj = GoodsReturned.objects.get(pk=receipt.pk)
        item_amount = float(item.quantity) * float(item_unit.purchase_price)
        receipt_obj.total = receipt_obj.total - item_amount
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

