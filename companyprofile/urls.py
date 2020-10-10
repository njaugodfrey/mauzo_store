from django.urls import path

from . import views

app_name = 'companyprofile'

urlpatterns = [
    path(
        '', views.home, name='home_page'
    ),
]
