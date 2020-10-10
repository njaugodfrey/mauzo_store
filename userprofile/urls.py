from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'userprofile'


urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='userprofile/login.html'),
        name='login'
    ),
    path(
        'logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'
    ),
    path(
        'user/<str:slug>/', views.ProfileDetailView.as_view(),
        name='user-profile'
    ),
    path(
        'reset-password/', auth_views.PasswordResetView.as_view(),
        {'template_name': 'userprofile/password_reset_form.html'}, name='password_reset'
    ),
]
