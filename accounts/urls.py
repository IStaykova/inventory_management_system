from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.forms import AppUserLoginForm
from accounts.views import RegisterView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='accounts/login-page.html',
        authentication_form = AppUserLoginForm,
        ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]