from django import forms

from inventory.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'image', 'category',]

        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                }),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'stock_quantity': forms.NumberInput(attrs={"class": "form-control"}),
            'image': forms.FileInput(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-select"}),
        }

class ProductDeleteForm(ProductForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True