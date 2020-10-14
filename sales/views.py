import json, csv

from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.db.models import Sum, Q

from .forms import *
from .filters import SalesFilter
from .models import SalesReceipt, SoldGoods, SalesReceiptVoid
from inventory.models import Stock, UnitOfMeasurement
from companyprofile.models import Company
from customer.models import Customer
from mauzo.decorators import allowed_user


# Create your views here.

# sales receipt
@login_required
def receipts_list(request):
    receipts = SalesReceipt.objects.all().order_by('-receipt_number')
    receipts_filter = SalesFilter(request.GET, queryset=receipts)
    context = {
        'all_receipts': receipts,
        'filter': receipts_filter
    }
    return render(
        request, template_name='sales/receipts_list.html',
        context=context
    )


def filter_receipts(request):
    if 'q' in request.GET:
        query = request.GET['q']
        date_obj = datetime.strptime(query, '%d-%m-%Y')

        receipts = SalesReceipt.objects.filter(
            sale_date__icontains=query
        )

        context = {
            'receipts': receipts
        }
        return render(
            request, template_name='sales/filtered_receipts.html',
            context=context
        )


def print_sales(request):
    sales = SalesReceipt.objects.all


@login_required
def create_sales_receipt(request):
    form = SalesReceiptForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        last_receipt = SalesReceipt.objects.all().order_by('receipt_number').last()
        if not last_receipt:
            obj.receipt_number = 'CS' + str(datetime.today().month).zfill(2) + \
                                 str(datetime.today().day).zfill(2) + '001'
        else:
            receipt_number = last_receipt.receipt_number
            receipt_int = int(receipt_number[7:11])
            new_receipt_int = receipt_int + 1
            new_receipt_number = 'CS' + str(datetime.today().month).zfill(2) + \
                                 str(datetime.today().day).zfill(2) + str(new_receipt_int).zfill(4)
            obj.receipt_number = new_receipt_number

        obj.sale_date = datetime.today()
        # if obj.debtors_account: obj.is_credit = True
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


# sales invoice
@login_required
@allowed_user(['Accounts'])
def create_sales_invoice(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    last_receipt = SalesReceipt.objects.all().order_by('receipt_number').last()
    if not last_receipt:
        receipt_number = 'SI' + str(datetime.today().month).zfill(2) + \
                             str(datetime.today().day).zfill(2) + '001'
    else:
        receipt_number = last_receipt.receipt_number
        receipt_int = int(receipt_number[7:11])
        new_receipt_int = receipt_int + 1
        new_receipt_number = 'SI' + str(datetime.today().month).zfill(2) + \
                             str(datetime.today().day).zfill(2) + str(new_receipt_int).zfill(4)
        receipt_number = new_receipt_number
    sale_date = datetime.today()
    is_credit = True
    salesman = request.user

    new_invoice = SalesReceipt(
        sale_date=sale_date,
        receipt_number=receipt_number,
        is_credit=is_credit,
        debtors_account=customer,
        salesman=salesman
    )
    new_invoice.save()
    return redirect(
        'sales:view_receipt', slug=new_invoice.slug, pk=new_invoice.id
    )


@login_required
@allowed_user(['Accounts'])
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
def get_units(request):
    stock_id = request.GET.get('item')
    units = UnitOfMeasurement.objects.select_related().filter(stock_id=stock_id)
    return render(
        request, 'inventory/units_list.html',
        {'units': units}
    )


@login_required
def unit_values(request):
    unit_id = request.GET.get('unit')
    price = UnitOfMeasurement.objects.get(pk=unit_id).selling_price
    return render(
        request, 'sales/partial_price_list.html',
        {'price': price}
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
        sprice = UnitOfMeasurement.objects.get(pk=uom).selling_price
        response_data = {}

        if stock_item.quantity > 0 and stock_item.quantity >= float(quantity):
            # process the form
            receipt_item = SoldGoods(
                receipt_ref=SalesReceipt.objects.get(id=pk),
                product=Stock.objects.get(pk=item),
                quantity=quantity,
                unit_of_measurement=UnitOfMeasurement.objects.get(pk=uom),
                price=sprice,
                vat=round(float(vat) * float(sprice)) / float(100 + float(vat)),
                amount=float(quantity) * float(sprice)
            )
            receipt_item.save()

            # update receipt total
            receipt = SalesReceipt.objects.get(id=pk)
            item_amount = float(quantity) * float(sprice)
            receipt.total = receipt.total + item_amount
            receipt.save()

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


@csrf_exempt
@login_required
def remove_receipt_items(request):
    if request.method == 'DELETE':
        item = SoldGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_product = item.product
        item.delete()
        product_obj = Stock.objects.get(pk=item_product.pk)
        product_obj_quantity = product_obj.quantity
        product_obj.quantity = int(product_obj_quantity) - int(item.quantity)
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

    with open("receipt.txt", "w") as rcpt:
        response = HttpResponse()
        response['content_type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=receipt.txt'
        response.writelines(
            [company.company_name + '\n',
             company.telephone_1 + '\n',
             company.telephone_2 + '\n',
             company.kra_pin + '\n',
             company.kra_vat + '\n'],
        )
        response.writelines([
            receipt.receipt_number + '\n',
            str(receipt.sale_date.strftime("%d/%m/%Y, %H:%M:%S")) + '\n'
        ])
        response.write('-----------------------------------------\n')
        response.writelines([
            'Code\t', 'Qty\t', 'Price\t', 'Tax\t', 'Amount\n'
        ])
        for item in items:
            response.write(item.product.stock_name + ' - ' + item.unit_of_measurement.unit_name + '\n')
            response.writelines([
                item.product.stock_code + '\t',
                str(item.quantity) + '\t',
                str(item.price) + '\t',
                str(item.product.stock_vat_code.vat_code) + '\t',
                str(item.amount) + '\n'
            ])
        response.write('-----------------------------------------\n')
        response.write('Total\t\t\t\t' + str(receipt.total) + '\n')
        response.write('-----------------------------------------\n')
        tax_items = items.values('product__stock_vat_code__vat_code').annotate(Sum('vat'))
        for result in tax_items:
            result
            '''for key in result:
                response.write(result[key])'''

        response.write('-----------------------------------------\n')
        response.write('You were served by: ' + str(receipt.salesman).upper() + '\n')
        response.write('-----------------------------------------\n')
        response.write('Prices inclusive of VAT where applicable')
        response.writelines('\n')
        # Duplicate
        response.write('-----------------------------------------\n')
        response.write('\t\t Copy \n')
        response.write('-----------------------------------------\n')
        response.write('Receipt No:' + receipt.receipt_number + '\n')
        response.write(
            'Sale date: ' + str(receipt.sale_date.strftime("%d/%m/%Y")) + '\n'
        )
        response.write('Amount: ' + str(receipt.total))
        response.write('Salesman: ' + str(receipt.salesman).upper() + '\n')

    return response


# void a sale
@csrf_exempt
@login_required
def sales_returns(request, pk, slug, item_pk):
    if request.method == 'POST':
        item = request.POST.get('item')
        sale_item = request.POST.get('saleItem')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        uom = request.POST.get('uom')

        return_rcpt = SoldGoods.objects.get(pk=sale_item)
        return_rcpt.void_sale = True
        return_rcpt.save()
        response_data = {}

        return_item = SalesReceiptVoid(
            receipt_ref=SalesReceipt.objects.get(pk=return_rcpt.receipt_ref.pk),
            sale_item_ref=SoldGoods.objects.get(pk=sale_item),
            product=Stock.objects.get(pk=return_rcpt.product.pk),
            quantity=-int(return_rcpt.quantity),
            unit_of_measurement=UnitOfMeasurement.objects.get(pk=return_rcpt.unit_of_measurement.pk),
            price=-return_rcpt.price,
            amount=-int(return_rcpt.quantity) * int(float(return_rcpt.price))
        )
        return_item.save()

        stock_item = Stock.objects.get(stock_name=item)
        stock_item_quantity = stock_item.quantity
        stock_item.quantity = int(stock_item_quantity) + int(return_rcpt.quantity)
        stock_item.save()

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


@csrf_exempt
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

    with open("void_receipt.txt", "w") as rcpt:
        response = HttpResponse()
        response['content_type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=void_receipt.txt'
        response.writelines(
            [company.company_name + '\n',
             company.telephone_1 + '\n',
             company.telephone_2 + '\n',
             company.kra_pin + '\n',
             company.kra_vat + '\n'],
        )
        response.writelines([
            receipt.receipt_number + '\n',
            str(receipt.sale_date) + '\n'
        ])
        response.write('--------------------------------\n')
        response.writelines([
            'Code\t', 'Description\t', 'Qty\t', 'Price\t', 'Tax\t', 'Amount\n'
        ])
        for item in items:
            response.write(item.product.stock_name + ' - ' + item.unit_of_measurement.unit_name + '\n')
            response.writelines([
                item.product.stock_code + '\t\t',
                str(item.quantity) + '\t\t',
                str(item.price) + '\t',
                str(item.product.stock_vat_code.vat_code) + '\t',
                str(item.amount) + '\n'
            ])

    return response
