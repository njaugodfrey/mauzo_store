from django.conf.urls import url
from django.urls import path, include

from . import views
from . import creditsales

app_name = 'sales'

urlpatterns = [
    # sales receipts
    path(
        'receipts/all/', views.receipts_list, name='all_receipts'
    ),
    path(
        'receipts/new-receipt/', views.create_sales_receipt,
        name='new_receipt'
    ),
    path(
        'receipts/<slug>-<pk>/details', views.sales_receipt_detail,
        name='view_receipt'
    ),
    path(
        'receipts/<slug>-<pk>/update', views.update_sales_receipt,
        name='update_receipt'
    ),
    path(
        'receipts/print/receipt/<int:pk>/', views.print_sales_receipt,
        name='print-receipt'
    ),
    path(
        'invoices/new-invoice/<pk>', views.create_sales_invoice,
        name='new_invoice'
    ),
    path(
        'receipts/all/filter/', views.filter_receipts,
        name='filter_receipts'
    ),
    path(
        'receipts/all/search/', views.search_receipts,
        name='search_receipts'
    ),
    # Sold goods urls
    path(
        'receipt/<str:slug>-<int:pk>/add-item',
        views.add_receipt_items, name='new-product'
    ),
    path(
        'receipt/remove-item/',
        views.remove_receipt_items, name='remove-product'
    ),
    path(
        'receipt/unit-of-measurement/price',
        views.unit_values, name='unit-values'
    ),
    # sales returns/void
    path(
        'returns/<str:slug>-<int:pk>/return-item/<int:item_pk>/',
        views.sales_returns, name='return-product'
    ),
    path(
        'returns/<str:slug>-<int:pk>/void',
        views.sales_returns_detail, name='sales_returns'
    ),
    path(
        'returns/print/return/<int:pk>/',
        views.print_sales_returns, name='print-return'
    ),
    path(
        'receipts/print/decoy/<int:pk>/', views.print_decoy_receipt,
        name='print-decoy'
    ),
    # sales invoices
    path(
        'invoices/new-invoice/', creditsales.create_sales_invoice,
        name='new-invoice'
    ),

]
