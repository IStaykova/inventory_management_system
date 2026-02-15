from django import forms

from inventory.models import Product
from orders.models import Order

# Single product order form, with dynamic quantity choices based on product stock
# class CreateOrderForm(forms.ModelForm):
#     quantity = forms.ChoiceField(
#         choices=(),
#         widget=forms.Select(attrs={"class": "form-select"})
#     )
#     class Meta:
#         model = Order
#         fields = ['customer_name']
#         widgets = {'customer_name': forms.TextInput(attrs={"class": "form-control"}),}
#
#     def __init__(self, *args, **kwargs):
#         product = kwargs.pop("product", None)
#         super().__init__(*args, **kwargs)
#
#         self.fields["quantity"].choices = [
#             (str(i), str(i)) for i in range(1, product.stock_quantity + 1)
#         ]

class OrderCustomerForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control"})
        }

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