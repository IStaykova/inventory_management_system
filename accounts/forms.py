from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

UserModel = get_user_model()

class AppUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username')

class AppUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    widgets = {
        'email': forms.EmailInput(attrs={"class": "form-control"}),
        'password': forms.PasswordInput(attrs={"class": "form-control"}),
    }
    error_messages = {
        'invalid_login': 'Invalid email or password.',
        'inactive': 'This profile is not active',
    }
