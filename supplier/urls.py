from django.urls import path

from . import views

app_name = 'supplier'

urlpatterns = [
    path(
        '', views.suppliers_list,
        name='all_suppliers'
    ),
    path(
        'create/', views.create_supplier,
        name='new_supplier'
    ),
    path(
        '<str:slug>-<pk>/', views.supplier_detail,
        name='supplier_detail'
    ),
    path(
        '<str:slug>-<pk>/update/',
        views.update_supplier, name='supplier_update'
    ),
    path(
        '<pk>/delete/',
        views.delete_supplier, name='supplier_delete'
    ),
]
