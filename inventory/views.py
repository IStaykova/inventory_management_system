from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from inventory.models import Product


def home_page(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, 'inventory/home-page.html', {'products': products})

def product_details(request: HttpRequest, pk) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product-details-page.html', {'product': product})

