from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.LicensesView, name='index'),
    path('licenses', views.LicensesView, name='licenses'),
    path('login', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view(next_page='/')),

]
