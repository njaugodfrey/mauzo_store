import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.utils.timezone import datetime
from django.contrib.auth.decorators import login_required

from .models import (
    StockWriteOn, StockWriteOff, Stock,
    GoodsWrittenOn, GoodsWrittenOff, UnitOfMeasurement,
    StockCardEntry
)
from .forms import WriteOnForm, WriteOffForm
from mauzo.decorators import allowed_user


# writeons
@login_required
@allowed_user(['Accounts'])
def create_write_on(request):
    last_write_on = StockWriteOn.objects.all().order_by('write_on_number').last()
    if not last_write_on:
        write_on_number = 'WON-' + str(1).zfill(4)
    else:
        document_number = last_write_on.write_on_number
        document_int = int(document_number[4:])
        new_document_int = document_int + 1
        new_document_number = 'WON-' + str(new_document_int).zfill(4)
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
@allowed_user(['Accounts'])
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

        # log in stock card
        stock_card = StockCardEntry(
            stock=Stock.objects.get(pk=item),
            document=StockWriteOn.objects.get(id=pk).write_on_number,
            quantity=float(quantity) * float(item_unit.base_quantity),
            unit=item_unit,
            price=0,
            amount=0
        )
        stock_card.save()
        write_on_item.log_number = stock_card.pk
        write_on_item.save()

        # data to respond with
        response_data = {
            'result': 'Item saved successfully',
            'item_id': write_on_item.pk,
            'item_name': write_on_item.stock.stock_name,
            'item_quantity': write_on_item.quantity
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
@allowed_user(['Accounts'])
def remove_writeon_item(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = GoodsWrittenOn.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_product = item.stock
        item_unit = item.unit_of_measurement
        entry = StockCardEntry.objects.get(pk=item.log_number)
        entry.delete()
        item.delete()
        stock_obj = Stock.objects.get(pk=item_product.pk)
        stock_obj_quantity = stock_obj.quantity
        remove_quantity = float(item_unit.base_quantity) * float(item.quantity)
        stock_obj.quantity = float(stock_obj_quantity) - float(remove_quantity)
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


# write off
@login_required
@allowed_user(['Accounts'])
def create_write_off(request):
    last_write_off = StockWriteOff.objects.all().order_by('write_off_number').last()
    if not last_write_off:
        write_off_number = 'WOF-' + str(1).zfill(4)
    else:
        document_number = last_write_off.write_off_number
        document_int = int(document_number[4:])
        new_document_int = document_int + 1
        new_document_number = 'WOF-' + str(new_document_int).zfill(4)
        write_off_number = new_document_number
    write_off_date = datetime.today()
    input_by = request.user

    new_write_off = StockWriteOff(
        write_off_date=write_off_date,
        write_off_number=write_off_number,
        input_by=input_by
    )
    new_write_off.save()
    return redirect(
        'inventory:writeoff-detail',
        slug=new_write_off.slug, pk=new_write_off.pk
    )


@login_required
@allowed_user(['Accounts'])
def write_off_list(request):
    context = {
        'writeoffs': StockWriteOff.objects.order_by('write_off_date').all()
    }
    return render(
        request, template_name='inventory/write_off_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def write_off_detail(request, pk, slug):
    form = WriteOffForm(request.POST or None)
    write_off = get_object_or_404(StockWriteOff, pk=pk)
    items = GoodsWrittenOff.objects.filter(document_ref=write_off.id).select_related()

    context = {
        'form': form,
        'writeoff': write_off,
        'items': items
    }
    return render(
        request, template_name='inventory/stock_write_off.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def add_write_off_item(request, pk, slug):
    if request.method == 'POST':
        item = request.POST.get('item')
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')

        # process form
        write_off_item = GoodsWrittenOff(
            document_ref=StockWriteOff.objects.get(id=pk),
            stock=Stock.objects.get(pk=item),
            quantity=quantity,
            unit_of_measurement=UnitOfMeasurement.objects.get(pk=unit)
        )
        write_off_item.save()

        # update stock quantity
        item_unit = UnitOfMeasurement.objects.get(pk=unit)
        stock_item = Stock.objects.get(pk=item)
        stock_writen_off = float(item_unit.base_quantity) * float(quantity)
        stock_item.quantity = stock_item.quantity - stock_writen_off
        stock_item.save()

        # log in stock card
        stock_card = StockCardEntry(
            stock=Stock.objects.get(pk=item),
            document=StockWriteOff.objects.get(id=pk).write_off_number,
            quantity=-(float(quantity) * float(item_unit.base_quantity)),
            unit=item_unit,
            price=0,
            amount=0
        )
        stock_card.save()
        write_off_item.log_number = stock_card.pk
        write_off_item.save()

        # data to respond with
        response_data = {
            'result': 'Item saved successfully',
            'item_id': write_off_item.pk,
            'item_name': write_off_item.stock.stock_name,
            'item_quantity': write_off_item.quantity
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
@allowed_user(['Accounts'])
def remove_write_off_item(request, pk, slug, item_pk):
    if request.method == 'DELETE':
        item = GoodsWrittenOff.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_product = item.stock
        item_unit = item.unit_of_measurement
        entry = StockCardEntry.objects.get(pk=item.log_number)
        entry.delete()
        item.delete()
        stock_obj = Stock.objects.get(pk=item_product.pk)
        stock_obj_quantity = stock_obj.quantity
        remove_quantity = float(item_unit.base_quantity) * float(item.quantity)
        stock_obj.quantity = float(stock_obj_quantity) + float(remove_quantity)
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
