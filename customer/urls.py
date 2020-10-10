from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [
    path(
        '', views.customers_list, name='customers_list'
    ),
    path(
        'create/', views.create_customer, name='new_customer'
    ),
    path(
        '<str:slug>-<pk>/', views.customer_detail,
        name='customer_detail'
    ),
    path(
        '<str:slug>-<pk>/update/', views.update_supplier,
        name='update_customer'
    ),
]