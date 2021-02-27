from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.LicensesView, name='index'),
    path('licenses', views.LicensesView, name='licenses'),
    path('createusers', views.CreateUsers, name='createusers'),
    path('login', LoginView.as_view(template_name='login.html')),
    path('accounts/login/', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('accounts/profile/', views.LicensesView, name='profile'),
    path('add', views.AddLicense, name='addlicense'),
    path('add_user_licenses', views.AddUserLicenses, name='adduserlicenses'),
    path('admin/', views.AdminView, name='admin'),
    path('admin/api/v1/hidden/allaccountsview/', views.AllAccountsView, name='allaccountsview'),

]
