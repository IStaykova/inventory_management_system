from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileForm, AddressForm
from accounts.models import Profile, Address

User = get_user_model()

class RegisterView(CreateView):
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('accounts:login')

class AppLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password-change-page.html'
    success_url = reverse_lazy('accounts:profile_details')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password-change-done-page.html'

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user = User
        return user.objects.get(pk=self.request.user.pk).profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_address'] = Address.objects.filter(user=self.request.user).first()
        return context

def profile_update_view(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        address_user = Address.objects.filter(user__id=request.user.id).first()
        form = ProfileForm(request.POST or None, instance=current_user)
        address_form = AddressForm(request.POST or None, instance=address_user)

        if form.is_valid() and address_form.is_valid():
            form.save()
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile_details')
        return render(request, 'accounts/profile-update-page.html', {'form': form, 'address_form': address_form})
    else:
        messages.success(request, 'You need to be logged in to update your profile.')
        return redirect('accounts:login')




