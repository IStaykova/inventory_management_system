from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from accounts.forms import AppUserLoginForm
from accounts.views import RegisterView, ProfileDetailView, profile_update_view, CustomPasswordChangeView, \
    CustomPasswordChangeDoneView, PasswordResetRequestView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='accounts/login-page.html',
        authentication_form = AppUserLoginForm,
        ), name='login'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/details', ProfileDetailView.as_view(), name='profile_details'),
    path('profile/update/', profile_update_view, name='profile_update'),


    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password-reset-done-page.html",
        ),name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password-reset-confirm-page.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password-reset-complete-page.html"), name="password_reset_complete"),

]