from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # stocks
    path(
        'stocks/', views.stocks_list, name='stocks_list'
    ),
    path(
        'stocks/<slug>-<pk>/', views.stock_detail,
        name='stock_detail' 
    ),
    path(
        'stocks/create/', views.create_stock,
        name='create_item'
    ),
    path(
        'stocks/<slug>-<pk>/update/', views.update_stock,
        name='stock_update'
    ),
    # units of measurement
    path(
        'units-of-measurement/all', views.units_list,
        name='all-units'
    ),
    path(
        'units-of-measurement/<int:pk>/',
        views.unit_detail, name='unit-detail'
    ),
    path(
        'units-of-measurement/new',
        views.create_unit, name='unit-create'
    ),
    path(
        'units-of-measurement/<int:pk>/update',
        views.update_unit, name='unit-update'
    ),
    path(
        'units-of-measurement/<int:pk>',
        views.UnitDelete.as_view(), name='unit-delete'
    ),
    # Goods receipts
    path(
        'goods-receipt/create-new/',
        views.create_goods_receipt, name='new-goods-receipt'
    ),
    path(
        'goods-receipt/grn-list/',
        views.goods_receipts_list, name='goods-receipts-list'
    ),
    path(
        'goods-receipt/<str:slug>/<int:pk>/',
        views.goods_receipt_details, name='goods-receipt-detail'
    ),
    path(
        'goods-receipt/<str:slug>-<int:pk>/add-item',
        views.add_receipt_items, name='new-item'
    ),
    path(
        'goods-receipt/<str:slug>-<int:pk>/remove-item/<int:item_pk>/',
        views.remove_receipt_items, name='remove-item'
    ),
    path(
        'goods-receipt/units-of-measurement/',
        views.get_units, name='uom-list'
    ),
    # Goods returns
    path(
        'goods-returns/create-new/',
        views.create_returns, name='new-goods-returns'
    ),
    path(
        'goods-returns/grn-list/',
        views.goods_returns_list, name='goods-returns-list'
    ),
    path(
        'goods-returns/<str:slug>/<int:pk>/',
        views.goods_returns_detail, name='goods-returns-detail'
    ),
    path(
        'goods-returns/<str:slug>-<int:pk>/add-item',
        views.add_returns_items, name='return-item'
    ),
    path(
        'goods-returns/<str:slug>-<int:pk>/delete-item/<int:item_pk>/',
        views.remove_returns_items, name='delete-item'
    ),
]
