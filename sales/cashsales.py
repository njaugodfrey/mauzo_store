import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import datetime
from tabulate import tabulate

from companyprofile.models import Company
from inventory.models import (
    Stock, UnitOfMeasurement,
    StockCardEntry
)
from .forms import SalesReceiptForm, SoldGoodsForm
from .models import SalesReceipt, SoldGoods, SalesReceiptVoid


@login_required
def create_sales_receipt(request):
    form = SalesReceiptForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        last_receipt = SalesReceipt.objects.all().order_by('id').last()
        if not last_receipt:
            obj.receipt_number = 'CS' + str(datetime.today().month).zfill(2) + \
                                 str(datetime.today().day).zfill(2) + '001'
        else:
            receipt_number = last_receipt.receipt_number
            receipt_int = int(receipt_number[6:])
            new_receipt_int = receipt_int + 1
            new_receipt_number = 'CS' + str(datetime.today().month).zfill(2) + \
                                 str(datetime.today().day).zfill(2) + str(new_receipt_int).zfill(4)
            obj.receipt_number = new_receipt_number

        obj.sale_date = datetime.today()
        obj.salesman = request.user
        obj.save()
        return redirect(
            'sales:view_receipt', slug=obj.slug, pk=obj.id
        )

    context = {
        'form': form
    }
    return render(
        request, template_name='sales/create_sales_receipt.html',
        context=context
    )


@login_required
def update_sales_receipt(request, pk, slug):
    receipt = get_object_or_404(SalesReceipt, pk=pk)
    form = SalesReceiptForm(
        request.POST or None, instance=receipt
    )
    if form.is_valid():
        form.save()
        return redirect(
            'sales:view_receipt', slug=receipt.slug, pk=receipt.id
        )

    context = {
        'form': form
    }
    return render(
        request, template_name='sales/create_sales_receipt.html',
        context=context
    )


@login_required
def sales_receipt_detail(request, pk, slug):
    receipt = get_object_or_404(SalesReceipt, pk=pk)
    form = SoldGoodsForm(request.POST or None)
    items = SoldGoods.objects.filter(receipt_ref=receipt.id).select_related()

    context = {
        'receipt': receipt,
        'items': items,
        'form': form
    }
    return render(
        request, template_name='sales/receipt_detail.html',
        context=context
    )


@login_required
def add_receipt_items(request, pk, slug):
    if request.method == 'POST':
        # grab form values
        item = request.POST.get('item')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        uom = request.POST.get('uom')
        vat = Stock.objects.get(pk=item).stock_vat_code.code_percentage
        stock_item = Stock.objects.get(pk=item)
        item_unit = UnitOfMeasurement.objects.get(pk=uom)
        sprice = UnitOfMeasurement.objects.get(pk=uom).selling_price
        response_data = {}

        if stock_item.quantity > 0 and stock_item.quantity >= float(quantity):
            # process the form
            receipt_item = SoldGoods(
                receipt_ref=SalesReceipt.objects.get(id=pk),
                product=Stock.objects.get(pk=item),
                quantity=quantity,
                unit_of_measurement=item_unit,
                price=sprice,
                vat=round(float(vat) * float(quantity) * float(sprice)) / float(100 + float(vat)),
                amount=float(quantity) * float(sprice)
            )
            receipt_item.save()

            # update receipt total
            receipt = SalesReceipt.objects.get(id=pk)
            item_amount = float(quantity) * float(sprice)
            receipt.total = receipt.total + item_amount
            receipt.save()

            # log in stock card
            stock_card = StockCardEntry(
                stock=Stock.objects.get(pk=item),
                document=SalesReceipt.objects.get(id=pk).receipt_number,
                quantity=-float(quantity) * float(item_unit.base_quantity),
                unit=item_unit,
                price=sprice,
                amount=float(quantity) * float(sprice)
            )
            stock_card.save()
            receipt_item.log_number = stock_card.pk
            receipt_item.save()

            # update stock quantity
            stock_unit = UnitOfMeasurement.objects.get(pk=uom)
            sold_stock = float(stock_unit.base_quantity) * float(quantity)
            stock_item.quantity = stock_item.quantity - sold_stock
            stock_item.save()

            response_data['result'] = 'Item saved successfully'
            response_data['item_id'] = receipt_item.pk
            response_data['item_name'] = receipt_item.product.stock_name
            response_data['item_quantity'] = receipt_item.quantity
            response_data['item_uom'] = receipt_item.unit_of_measurement.unit_name
            response_data['item_price'] = receipt_item.price
            response_data['item_vat'] = round(receipt_item.vat, 2)
            response_data['total_cost'] = receipt_item.amount
            response_data['receipt_total'] = receipt.total

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        else:
            return HttpResponse(
                json.dumps({"nothing to see": "action not successful"}),
                content_type="application/json"
            )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "action not successful"}),
            content_type="application/json"
        )


@login_required
def remove_receipt_items(request):
    if request.method == 'DELETE':
        item = SoldGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_product = item.product
        item_unit = item.unit_of_measurement.base_quantity
        entry = StockCardEntry.objects.get(pk=item.log_number)
        entry.delete()
        item.delete()

        # update stock quantity
        product_obj = Stock.objects.get(pk=item_product.pk)
        product_obj_quantity = product_obj.quantity
        product_obj.quantity = float(product_obj_quantity) + \
                               float(item.quantity * item_unit)
        product_obj.save()

        # update receipt total
        receipt = SalesReceipt.objects.get(pk=item.receipt_ref.pk)
        receipt.total = receipt.total - item.amount
        receipt.save()

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


@login_required
def print_sales_receipt(request, pk):
    company = Company.objects.get(pk=1)
    receipt = SalesReceipt.objects.get(pk=pk)
    items = SoldGoods.objects.filter(receipt_ref=pk).select_related()
    tax = SoldGoods.objects.filter(receipt_ref=pk).select_related().aggregate(Sum('vat'))
    user = request.user
    print_time = datetime.now()

    with open("receipt.txt", "w") as rcpt:
        response = HttpResponse()
        response['content_type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=receipt.txt'

        response.write(company.company_name + '\n', )
        response.writelines([
            company.telephone_1, company.telephone_2 + '\n',
            'PIN: ', company.kra_pin, 'VAT', company.kra_vat + '\n'
        ])
        response.writelines([
            'Number: ' + receipt.receipt_number + '\n',
            'Created: ' + str(receipt.sale_date.strftime("%d-%m-%Y, %H:%M:%S")) + '\n',
            'Printed: ' + str(print_time.strftime("%d-%m-%Y, %H:%M:%S")) + '\n',
        ])
        if receipt.walkin_customer:
            response.write('Customer: ' + receipt.walkin_customer + '\n')
        response.write('----------------------------------------------\n')
        if receipt.printed:
            response.write('-----------  Receipt Duplicate  ---------\n')
        else:
            response.write('-------------- Tax Receipt --------------\n')
        response.write('----------------------------------------------\n')
        response.writelines([
            'Code       Qty      Price        Tax         Amount\n'
        ])

        items_table = []
        for item in items:
            response.write(item.product.stock_name + ' - ' + item.unit_of_measurement.unit_name + '\n')
            response.writelines([
                "{:<5}       {:<4}     {:<7}       {:<1}          {:<10}\n".format(
                    item.product.stock_code, str(int(item.quantity)),
                    str(item.price), str(item.product.stock_vat_code.vat_code),
                    str(item.amount)
                )
            ])
        response.write('-----------------------------------------\n')
        # for vat in tax:
        exclusive = (tax.get('vat__sum')) / 0.16
        response.write('VAT:               ' + str(round(tax.get('vat__sum'), 2)) + '\n')
        response.write('Taxable exclusive: ' + str(
            round(exclusive, 2)
        ) + '\n')
        exempt = receipt.total - (exclusive + tax.get('vat__sum'))
        response.write('Exempt:            ' + str(round(exempt, 2)) + '\n')
        response.write('Total:             ' + str(receipt.total) + '\n')
        response.write('-----------------------------------------\n')

        response.write('You were served by: ' + str(receipt.salesman).upper() + '\n')
        response.write('Prices inclusive of VAT where applicable\n\n')

        # Duplicate
        if receipt.printed == False:
            response.write('------------ Receipt Copy ---------------\n')
            response.write('-----------------------------------------\n')
            response.write('Receipt No:' + receipt.receipt_number + '\n')
            response.write(
                'Sale date: ' + str(receipt.sale_date.strftime("%d/%m/%Y")) + '\n'
            )
            response.write('Amount: ' + str(receipt.total) + '\n')
            response.write('Salesman: ' + str(receipt.salesman).upper() + '\n')
            if receipt.walkin_customer:
                response.write('Customer: ' + receipt.walkin_customer + '\n')

        receipt.printed = True
        receipt.save()

    return response


# void a sale
@login_required
def sales_returns(request, pk, slug, item_pk):
    if request.method == 'POST':
        item = SoldGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )

        return_rcpt = SoldGoods.objects.get(pk=item.pk)
        return_rcpt.void_sale = True
        return_rcpt.save()
        response_data = {}

        return_item = SalesReceiptVoid(
            receipt_ref=SalesReceipt.objects.get(
                pk=return_rcpt.receipt_ref.pk
            ),
            sale_item_ref=SoldGoods.objects.get(pk=item.pk),
            product=Stock.objects.get(pk=return_rcpt.product.pk),
            quantity=-float(return_rcpt.quantity),
            unit_of_measurement=UnitOfMeasurement.objects.get(
                pk=return_rcpt.unit_of_measurement.pk
            ),
            price=-return_rcpt.price,
            amount=-float(return_rcpt.quantity) * float(float(return_rcpt.price))
        )
        return_item.save()

        # update inventory quantity
        stock_item = Stock.objects.get(pk=item.product.pk)
        stock_item_quantity = stock_item.quantity
        stock_item_unit = item.unit_of_measurement.base_quantity
        stock_item.quantity = float(stock_item_quantity) + \
                              float(return_rcpt.quantity * stock_item_unit)
        stock_item.save()

        # log in stock card
        stock_card = StockCardEntry(
            stock=Stock.objects.get(pk=return_rcpt.product.pk),
            document='void - ' + SalesReceipt.objects.get(
                pk=return_rcpt.receipt_ref.pk
            ).receipt_number,
            quantity=float(return_rcpt.quantity),
            unit=UnitOfMeasurement.objects.get(
                pk=return_rcpt.unit_of_measurement.pk
            ),
            price=float(return_rcpt.price),
            amount=-float(return_rcpt.quantity) * float(float(return_rcpt.price))
        )
        stock_card.save()
        return_item.log_number = stock_card.pk
        return_item.save()

        response_data['result'] = 'Item saved successfully'
        response_data['item_id'] = return_item.pk
        response_data['item_name'] = return_item.product.stock_name
        response_data['item_quantity'] = return_item.quantity
        response_data['item_uom'] = return_item.unit_of_measurement.unit_name
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
def sales_returns_detail(request, slug, pk):
    receipt = get_object_or_404(SalesReceipt, pk=pk)
    items = SoldGoods.objects.filter(receipt_ref=receipt.id).select_related()
    returned_items = SalesReceiptVoid.objects.filter(receipt_ref=receipt.id).select_related()

    context = {
        'receipt': receipt,
        'items': items,
        'returned_items': returned_items
    }
    return render(
        request, 'sales/void_sales_receipt.html',
        context
    )


@login_required
def print_sales_returns(request, pk):
    company = get_object_or_404(Company, pk=1)
    receipt = get_object_or_404(SalesReceipt, pk=pk)
    items = SalesReceiptVoid.objects.filter(receipt_ref=pk).select_related()
    tax = SalesReceiptVoid.objects.filter(receipt_ref=pk).select_related().aggregate(Sum('vat'))
    void_total = SalesReceiptVoid.objects.filter(receipt_ref=pk).select_related().aggregate(Sum('amount'))
    print_time = datetime.now()

    with open("void_receipt.txt", "w") as rcpt:
        response = HttpResponse()
        response['content_type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=void_receipt.txt'
        response.write(company.company_name + '\n', )
        header_table = [
            [company.telephone_1, company.telephone_2],
            ['PIN: ', company.kra_pin, 'VAT: ', company.kra_vat],
            []
        ]
        response.write(tabulate(header_table))
        response.writelines([
            '\nNumber: ' + receipt.receipt_number + '\n',
            'Printed: ' + str(print_time.strftime("%d-%m-%Y, %H:%M:%S")) + '\n',
        ])
        if receipt.walkin_customer:
            response.write('Customer: ' + receipt.walkin_customer + '\n')
        response.write('-----------------------------------------\n')
        response.write('-------------- Tax Receipt --------------\n')
        response.write('-----------------------------------------\n')
        response.writelines([
            'Code       Qty      Price        Tax         Amount\n'
        ])
        for item in items:
            response.write(item.product.stock_name + ' - ' + item.unit_of_measurement.unit_name + '\n')
            response.writelines([
                item.product.stock_code + '       ',
                str(item.quantity) + '      ',
                str(item.price).rjust(5) + '   ',
                str(item.product.stock_vat_code.vat_code) + '   ',
                str(item.amount).ljust(20) + '\n'
            ])
        response.write('-----------------------------------------\n')
        # for vat in tax:
        response.write('Tax:          ' + str(round(tax.get('vat__sum'), 2)) + '\n')
        inclusive = (tax.get('vat__sum')) / 0.16
        response.write('Taxable exclusive: ' + str(
            round(inclusive, 2)
        ) + '\n')
        exempt = void_total.get('amount__sum') - (inclusive + tax.get('vat__sum'))
        response.write('Exclusive:         ' + str(round(exempt, 2)) + '\n')
        response.write('Total:        ' + str(void_total.get('amount__sum')) + '\n')
        response.write('-----------------------------------------\n')

        response.write('You were served by: ' + str(receipt.salesman).upper() + '\n')
        response.write('Prices inclusive of VAT where applicable\n\n')

        # Duplicate
        response.write('------------ Receipt Copy ---------------\n')
        response.write('-----------------------------------------\n')
        response.write('Receipt No:' + receipt.receipt_number + '\n')
        response.write(
            'Sale date: ' + str(receipt.sale_date.strftime("%d/%m/%Y")) + '\n'
        )
        response.write('Amount: ' + str(receipt.total) + '\n')
        response.write('Salesman: ' + str(receipt.salesman).upper() + '\n')
        if receipt.walkin_customer:
            response.write('Customer: ' + receipt.walkin_customer + '\n')

    return response

