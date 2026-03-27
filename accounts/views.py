from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileForm
from accounts.models import Profile

User = get_user_model()

class RegisterView(CreateView):
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('accounts:login')

class AppLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user = User
        return user.objects.get(pk=self.request.user.pk).profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile-update-page.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        user = User
        return user.objects.get(pk=self.request.user.pk).profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile_details')
