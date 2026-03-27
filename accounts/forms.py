from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import Profile, Address

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'profile_picture', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'date_of_birth': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code']
        widgets = {
            'street': forms.TextInput(attrs={"class": "form-control"}),
            'city': forms.TextInput(attrs={"class": "form-control"}),
            'postal_code': forms.TextInput(attrs={"class": "form-control"}),
        }