from django import forms

from inventory.models import Product
from orders.models import Order

class OrderCustomerForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name"]
        widgets = {"customer_name": forms.TextInput(attrs={"class": "form-control"})}

class OrderAddProductForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(stock_quantity__gt=0),
        widget=forms.Select(attrs={"class": "form-select"}))

    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        quantity = cleaned_data.get("quantity")

        if product and quantity and quantity > product.stock_quantity:
                self.add_error("quantity", 'Not enough quantity available!')
        return cleaned_data

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        widgets = {"status": forms.Select(attrs={"class": "form-select"})}
