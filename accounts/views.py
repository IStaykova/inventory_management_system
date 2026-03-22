from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import AppUserCreationForm, AppUserLoginForm


class RegisterView(CreateView):
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('accounts:login')

class AppLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'
