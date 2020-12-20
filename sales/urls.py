from django.urls import path

from . import views, creditsales, cashsales

app_name = 'sales'

urlpatterns = [
    # sales receipts general
    path(
        'receipts/all/', views.receipts_list, name='all_receipts'
    ),
    path(
        'receipts/all/filter/', views.filter_receipts,
        name='filter_receipts'
    ),
    path(
        'receipts/all/filter/<date1><date2>/print', views.print_filtered_receipts,
        name='print_filtered_receipts'
    ),
    path(
        'receipts/clear/', views.clear_receipt,
        name='clear-receipt'
    ),
    path(
        'receipts/credit/', views.credit_receipt,
        name='credit-receipt'
    ),
    path(
        'receipts/all/report/', views.make_report,
        name='make-report'
    ),
    # sales receipts functionality
    path(
        'receipts/new-receipt/', cashsales.create_sales_receipt,
        name='new_receipt'
    ),
    path(
        'receipts/<slug>-<pk>/details', cashsales.sales_receipt_detail,
        name='view_receipt'
    ),
    path(
        'receipts/<slug>-<pk>/update', cashsales.update_sales_receipt,
        name='update_receipt'
    ),
    path(
        'receipts/print/receipt/<int:pk>/', cashsales.print_sales_receipt,
        name='print-receipt'
    ),
    # Sold goods urls
    path(
        'receipt/<str:slug>-<int:pk>/add-item',
        cashsales.add_receipt_items, name='new-product'
    ),
    path(
        'receipt/remove-item/',
        cashsales.remove_receipt_items, name='remove-product'
    ),
    path(
        'receipt/unit-of-measurement/price',
        views.unit_values, name='unit-values'
    ),
    # sales returns/void
    path(
        'receipt/returns/<str:slug>-<int:pk>/return-item/<int:item_pk>/',
        cashsales.sales_returns, name='return-product'
    ),
    path(
        'receipt/returns/<str:slug>-<int:pk>/void',
        cashsales.sales_returns_detail, name='sales_returns'
    ),
    path(
        'receipt/returns/print/return/<int:pk>/',
        cashsales.print_sales_returns, name='print-return'
    ),
    # sales invoices
    path(
        'invoices/new-invoice/<pk>/', creditsales.create_sales_invoice,
        name='new-invoice'
    ),
    path(
        'invoices/list/', creditsales.invoices_list,
        name='invoices-list'
    ),
    path(
        'invoices/<slug>-<pk>/detail/',
        creditsales.sales_invoice_detail, name='invoice-detail'
    ),
    path(
        'invoices/<str:slug>-<int:pk>/add-item',
        creditsales.add_invoice_items, name='invoice-new-product'
    ),
    path(
        'invoices/remove-item/',
        creditsales.remove_invoice_items, name='invoice-remove-product'
    ),
    path(
        'invoices/print/<int:pk>/', creditsales.print_invoice,
        name='invoice-print'
    ),
    path(
        'invoice/returns/<str:slug>-<int:pk>/return-item/<int:item_pk>/',
        creditsales.invoice_sales_returns, name='return-invoice-item'
    ),
    path(
        'invoice/returns/<str:slug>-<int:pk>/return',
        creditsales.invoice_returns_detail, name='credit-note-details'
    ),
    path(
        'invoice/returns/print/return/<int:pk>/',
        cashsales.print_sales_returns, name='print-credit-note'
    ),
]
