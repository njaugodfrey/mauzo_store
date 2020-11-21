import json
from tabulate import tabulate

from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.db.models import Sum

from .forms import SoldGoodsForm
from .models import SalesInvoice, InvoiceGoodsReturns, InvoiceGoods
from inventory.models import Stock, UnitOfMeasurement
from accounts.cash_models import CashReceipt
from companyprofile.models import Company
from customer.models import Customer
from mauzo.decorators import allowed_user


@login_required
@allowed_user(['Accounts'])
def invoices_list(request):
    context = {'invoices': SalesInvoice.objects.all()}
    return render(
        request, template_name='sales/invoices_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def create_sales_invoice(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    last_invoice = SalesInvoice.objects.all().order_by('invoice_number').last()
    if not last_invoice:
        invoice_number = 'SI0001'
    else:
        invoice_number = last_invoice.invoice_number
        invoice_int = int(invoice_number[2:])
        new_invoice_int = invoice_int + 1
        new_invoice_number = 'SI' + str(new_invoice_int).zfill(4)
        invoice_number = new_invoice_number
    invoice_date = datetime.today()
    salesman = request.user

    new_invoice = SalesInvoice(
        invoice_date=invoice_date,
        invoice_number=invoice_number,
        customer=customer,
        salesman=salesman
    )
    new_invoice.save()
    return redirect(
        'sales:invoice-detail', slug=new_invoice.slug, pk=new_invoice.id
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
        request, template_name='sales/invoice_detail.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def add_invoice_items(request, pk, slug):
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
            invoice_item = InvoiceGoods(
                invoice_ref=SalesInvoice.objects.get(id=pk),
                product=Stock.objects.get(pk=item),
                quantity=quantity,
                unit_of_measurement=UnitOfMeasurement.objects.get(pk=uom),
                price=sprice,
                vat=round(float(vat) * float(quantity) * float(sprice)) / float(100 + float(vat)),
                amount=float(quantity) * float(sprice)
            )
            invoice_item.save()

            # update invoice total
            invoice = SalesInvoice.objects.get(id=pk)
            item_amount = float(quantity) * float(sprice)
            invoice.total = invoice.total + item_amount
            invoice.save()

            # update customer balance
            customer = get_object_or_404(Customer, pk=invoice.customer.pk)
            customer.balance = customer.balance + item_amount
            customer.save()

            # update stock quantity
            stock_unit = UnitOfMeasurement.objects.get(pk=uom)
            sold_stock = float(stock_unit.base_quantity) * float(quantity)
            stock_item.quantity = stock_item.quantity - sold_stock
            stock_item.save()

            response_data['result'] = 'Item saved successfully'
            response_data['item_id'] = invoice_item.pk
            response_data['item_name'] = invoice_item.product.stock_name
            response_data['item_quantity'] = invoice_item.quantity
            response_data['item_uom'] = invoice_item.unit_of_measurement.unit_name
            response_data['item_price'] = invoice_item.price
            response_data['item_vat'] = round(invoice_item.vat, 2)
            response_data['total_cost'] = invoice_item.amount
            response_data['receipt_total'] = invoice.total

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
def remove_invoice_items(request):
    if request.method == 'DELETE':
        item = InvoiceGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )
        item_product = item.product
        item_unit = item.unit_of_measurement.base_quantity
        item.delete()

        # update stock quantity
        product_obj = Stock.objects.get(pk=item_product.pk)
        product_obj_quantity = product_obj.quantity
        product_obj.quantity = float(product_obj_quantity) + \
            float(item.quantity * item_unit)
        product_obj.save()

        # update invoice total
        invoice = SalesInvoice.objects.get(pk=item.invoice_ref.pk)
        invoice.total = invoice.total - item.amount
        invoice.save()

        # update customer balance
        customer = get_object_or_404(Customer, pk=invoice.customer.pk)
        customer.balance = customer.balance - item.amount
        customer.save()

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
@allowed_user(['Accounts'])
def invoice_sales_returns(request, pk, slug, item_pk):
    if request.method == 'POST':
        item = InvoiceGoods.objects.get(
            pk=int(QueryDict(request.body).get('item_pk'))
        )

        return_invoice = InvoiceGoods.objects.get(pk=item.pk)
        return_invoice.void_sale = True
        return_invoice.save()
        response_data = {}

        return_item = InvoiceGoodsReturns(
            invoice_ref=SalesInvoice.objects.get(
                pk=return_invoice.invoice_ref.pk
            ),
            sale_item_ref=InvoiceGoods.objects.get(pk=item.pk),
            product=Stock.objects.get(pk=return_invoice.product.pk),
            quantity=-float(return_invoice.quantity),
            unit_of_measurement=UnitOfMeasurement.objects.get(
                pk=return_invoice.unit_of_measurement.pk
            ),
            price=-return_invoice.price,
            amount=-float(return_invoice.quantity) * float(float(return_invoice.price))
        )
        return_item.save()

        stock_item = Stock.objects.get(pk=item.product.pk)
        stock_item_quantity = stock_item.quantity
        stock_item_unit = item.unit_of_measurement.base_quantity
        stock_item.quantity = float(stock_item_quantity) + \
            float(return_invoice.quantity * stock_item_unit)
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


@login_required
@allowed_user(['Accounts'])
def invoice_returns_detail(request, slug, pk):
    invoice = get_object_or_404(SalesInvoice, pk=pk)
    items = InvoiceGoods.objects.filter(invoice_ref=invoice.id)
    returned_items = InvoiceGoodsReturns.objects.filter(invoice_ref=invoice.id).select_related()

    context = {
        'invoice': invoice,
        'items': items,
        'returned_items': returned_items
    }
    return render(
        request, 'sales/credit_sales_returns.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def print_invoice(request, pk):
    company = Company.objects.get(pk=1)
    invoice = SalesInvoice.objects.get(pk=pk)
    items = InvoiceGoods.objects.filter(invoice_ref=pk).select_related()
    tax = InvoiceGoods.objects.filter(invoice_ref=pk).select_related().aggregate(Sum('vat'))
    user = request.user
    customer = Customer.objects.get(customer_code=invoice.customer.customer_code)
    print_time = datetime.now()

    with open('invoice.txt', 'w') as invc:
        response = HttpResponse()
        response['content_type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=invoice.txt'
        f'{"Hi": <16} StackOverflow!'
        response.write(f'{"": <25}' + company.company_name +'\n')
        header_table = [
            [
                company.postal_address,
                company.telephone_1 + '/' + company.telephone_2,
            ],
            [
                'PIN: ' + company.kra_pin + '\n',
                'VAT: ' + company.kra_vat + '\n'
            ]
        ]
        response.write(tabulate(header_table, tablefmt='plain') + '\n')
        customer_table = [
            ['Customer', customer.customer_name],
            ['Phone', customer.phone_number],
            ['Balance', customer.balance],
        ]
        response.write(tabulate(customer_table, tablefmt='plain') + '\n')

        response.write(f'{"": <25}' + '*** Tax Invoice ***\n')

        items_table = []
        for item in items:
            items_table.append(
                [
                    item.product.stock_code,
                    item.product.stock_name + ' - ' + item.unit_of_measurement.unit_name,
                    str(item.quantity),
                    str(item.price),
                    str(item.vat),
                    str(item.amount)
                ]
            )
        response.write(tabulate(
            items_table,
            headers=['Code', 'Description', 'Qty', 'Price', 'Tax', 'Amount']
        ))

        response.write('\n-----------------------------------------\n')
        #for vat in tax:
        response.write('VAT:               ' + str(round(tax.get('vat__sum'), 2)) + '\n')
        exclusive = (tax.get('vat__sum'))/0.14
        response.write('Taxable exclusive: ' + str(
            round(exclusive, 2)
        ) + '\n')
        exempt = invoice.total - (exclusive + tax.get('vat__sum'))
        response.write('Exempt:            ' + str(round(exempt, 2)) + '\n')
        response.write('Total:             ' + str(invoice.total) + '\n')

    
    return response
