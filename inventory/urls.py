from django.urls import path
from . import views, stocktake, grn

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
        'units-of-measurement/stock-list',
        views.get_units, name='uom-list'
    ),
    # Goods receipts
    path(
        'goods-receipt/create-new/',
        grn.create_goods_receipt, name='new-goods-receipt'
    ),
    path(
        'goods-receipt/grn-list/',
        grn.goods_receipts_list, name='goods-receipts-list'
    ),
    path(
        'goods-receipt/<str:slug>/<int:pk>/',
        grn.goods_receipt_details, name='goods-receipt-detail'
    ),
    path(
        'goods-receipt/<str:slug>-<int:pk>/add-item',
        grn.add_receipt_items, name='new-item'
    ),
    path(
        'goods-receipt/<str:slug>-<int:pk>/remove-item/<int:item_pk>/',
        grn.remove_receipt_items, name='remove-item'
    ),
    # Goods returns
    path(
        'goods-returns/create-new/',
        grn.create_returns, name='new-goods-returns'
    ),
    path(
        'goods-returns/grn-list/',
        grn.goods_returns_list, name='goods-returns-list'
    ),
    path(
        'goods-returns/<str:slug>/<int:pk>/',
        grn.goods_returns_detail, name='goods-returns-detail'
    ),
    path(
        'goods-returns/<str:slug>-<int:pk>/add-item',
        grn.add_returns_items, name='return-item'
    ),
    path(
        'goods-returns/<str:slug>-<int:pk>/delete-item/<int:item_pk>/',
        grn.remove_returns_items, name='delete-item'
    ),
    # Writeon
    path(
        'write-on/new/', stocktake.create_write_on,
        name='new-writeon'
    ),
    path(
        'write-on/writeon-list/', stocktake.write_on_list,
        name='writeon-list'
    ),
    path(
        'write-on/<slug>-<pk>/detail/', stocktake.write_on_detail,
        name='writeon-detail'
    ),
    path(
        'write-on/<slug>-<pk>/add-items/',
        stocktake.add_write_on_items, name='writeon-item'
    ),
    path(
        'write-on/<str:slug>-<int:pk>/delete-item/<int:item_pk>/',
        stocktake.remove_writeon_item, name='remove-writeon-item'
    ),
    # write off
    path(
        'write-off/new/', stocktake.create_write_off,
        name='new-writeoff'
    ),
    path(
        'write-off/writeoff-list/', stocktake.write_off_list,
        name='writeoff-list'
    ),
    path(
        'write-off/<slug>-<pk>/detail/', stocktake.write_off_detail,
        name='writeoff-detail'
    ),
    path(
        'write-off/<slug>-<pk>/add-items/',
        stocktake.add_write_off_item, name='writeoff-item'
    ),
    path(
        'write-off/<str:slug>-<int:pk>/delete-item/<int:item_pk>/',
        stocktake.remove_write_off_item, name='remove-writeoff-item'
    ),
]
