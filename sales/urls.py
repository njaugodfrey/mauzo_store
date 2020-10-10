from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'sales'

urlpatterns = [
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
]
