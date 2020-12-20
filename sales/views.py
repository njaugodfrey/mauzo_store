import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.utils.timezone import datetime

from inventory.models import UnitOfMeasurement
from mauzo.decorators import allowed_user
from .forms import ReceiptsFilterForm, DateReportForm
from .models import SalesReceipt


# Create your views here.

"""
- These views are for sales in general. Those which involve sharing
modules with different kinds of views.
- Views for sales made on cash basis are written in cashsales.py
- Views for sales made on credit basis are written in creditsales.py
"""

# sales receipt
@login_required
def receipts_list(request):
    receipts = SalesReceipt.objects.all().order_by('-receipt_number')
    filter_form = ReceiptsFilterForm(request.POST or None)
    report_form = DateReportForm(request.POST or None)
    context = {
        'all_receipts': receipts,
        'filter_form': filter_form,
        'report_form': report_form
    }
    return render(
        request, template_name='sales/receipts_list.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def filter_receipts(request):
    if 'start_date' and 'close_date' in request.GET:
        date1 = datetime.strptime(request.GET['start_date'], '%Y-%m-%d %H:%M')
        date2 = datetime.strptime(request.GET['close_date'], '%Y-%m-%d %H:%M')
        receipts = SalesReceipt.objects.filter(
            sale_date__range=[date1, date2]
        ).order_by('sale_date')
    
    else:
        return redirect(
            'sales:all_receipts'
        )
    
    context = {
        'receipts': receipts,
        'date1': date1,
        'date2': date2
    }
    return render(
        request, template_name='sales/search_results.html',
        context=context
    )


@login_required
@allowed_user(['Accounts'])
def print_filtered_receipts(request, date1, date2):
    first = date1[0:19]
    second = date1[19:]
    date1 = datetime.strptime(first, '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime(second, '%Y-%m-%d %H:%M:%S')
    receipts = SalesReceipt.objects.filter(
        sale_date__range=[date1, date2]
    )
    with open("sales_report.txt", "w") as rcpt:
            response = HttpResponse()
            response['content_type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=sales_report.txt'
            response.write('\t Gathee Wholesalers Ltd \n')
            response.write('Sales report for ' + str(date1) + ' - ' + str(date2) + '\n')
            response.write('Time \t\tNumber \t\tAmount \n')
            for receipt in receipts:
                response.write(
                    str(receipt.sale_date.strftime("%H:%M:%S")) + '\t' + \
                    receipt.receipt_number + '\t' + \
                    str(receipt.total) + '\n'
                )

    context = {
        'receipts': receipts
    }
    return response


@login_required
@allowed_user(['Accounts'])
def clear_receipt(request):
    """
    docstring
    """
    if request.method == 'POST':
        receipt = SalesReceipt.objects.get(
            pk=int(QueryDict(request.body).get('receipt_pk'))
        )
        if receipt.is_cleared:
            receipt.is_cleared = False
            receipt.save()
            response_data = {"msg": 'Done'}
        else:
            receipt.is_cleared = True
            receipt.save()
            response_data = {"msg": 'Done'}
        return HttpResponse(
            json.dumps(response_data)
        )
    
    else:
        return HttpResponse(
            json.dumps(
                {'msg': 'failed'}
            )
        )


@login_required
@allowed_user(['Accounts'])
def credit_receipt(request):
    """
    docstring
    """
    if request.method == 'POST':
        receipt = SalesReceipt.objects.get(
            pk=int(QueryDict(request.body).get('receipt_pk'))
        )
        if receipt.is_credit:
            receipt.is_credit = False
            receipt.save()
            response_data = {'msg': 'done'}
        else:
            receipt.is_credit = True
            receipt.save()
            response_data = {'msg': 'done'}
        return HttpResponse(
            json.dumps(response_data)
        )
    
    else:
        return HttpResponse(
            json.dumps(
                {'msg': 'failed'}
            )
        )


@login_required
@allowed_user(['Accounts'])
def make_report(request):
    if 'report_date' in request.GET:
        date1 = datetime.strptime(request.GET['report_date'], '%Y-%m-%d %H:%M')
        receipts = SalesReceipt.objects.filter(
            sale_date__range=[date1]
        ).order_by('sale_date')
    
    else:
        return redirect(
            'sales:all_receipts'
        )
    
    context = {
        'receipts': receipts
    }
    return render(
        request, template_name='sales/dummy.html',
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
