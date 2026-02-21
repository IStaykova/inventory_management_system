from django import forms

from inventory.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'image', 'category']

        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control","rows": 4}),
            'price': forms.NumberInput(attrs={"class": "form-control", "min": "1", "step": "0.01"}),
            'stock_quantity': forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            'image': forms.FileInput(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            'name': { "required": "Please enter product name."},
            'price': { "required": "Please enter valid product price."},
            'stock_quantity': { "required": "Please enter stock quantity."},
        }

class SearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name...'})
    )