from django.urls import path

from . import cash_views

app_name = 'accounts'

urlpatterns = [
    # cash receipts
    path(
        'cash-receipt/all/', cash_views.cash_receipts_list,
        name='cash-receipts-list'
    ),
    path(
        'cash-receipt/new/', cash_views.create_cash_receipt,
        name='new-cash-receipt'
    ),
    path(
        'cash-receipt/new/<pk>/', cash_views.receipt_via_customer,
        name='receipt-customer'
    ),
    path(
        'cash-receipt/view/<slug>-<pk>/',
        cash_views.view_cash_receipt, name='cash-receipt-detail'
    ),
]
