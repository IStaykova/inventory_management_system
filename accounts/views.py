from itertools import product

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, DetailView, FormView

from accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileForm, AddressForm, PasswordResetRequestForm
from accounts.models import Profile, Address
from inventory_management_system import settings
from inventory_management_system.services.emails import send_template_email

User = get_user_model()

class RegisterView(CreateView):
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        send_template_email(
            to_email=self.object.email,
            template_id=settings.SENDGRID_REGISTER_TEMPLATE,
            dynamic_data={
                "name": self.object.username,
            },
        )
        return response

class AppLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password-change-page.html'
    success_url = reverse_lazy('accounts:profile_details')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password-change-done-page.html'

class PasswordResetRequestView(FormView):
    template_name = "accounts/password-reset-page.html"
    form_class = PasswordResetRequestForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = self.request.build_absolute_uri(
                reverse(
                    "accounts:password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token},
                )
            )
            app_link = self.request.build_absolute_uri(
                reverse("products:home")
            )
            send_template_email(
                to_email=user.email,
                template_id=settings.SENDGRID_CHANGE_PASSWORD_TEMPLATE,
                dynamic_data={
                    "name": user.username,
                    "reset_link": reset_link,
                    "app_link": app_link,
                },
            )
        return redirect("accounts:password_reset_done")

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




