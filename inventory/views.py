from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from inventory.forms import ProductForm
from inventory.models import Product

def home_page(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, 'inventory/product-list.html', {'products': products})

def product_details(request: HttpRequest, pk, slug) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk, slug=slug)
    return render(request, 'inventory/product-details-page.html', {'product': product})

def product_create(request: HttpRequest) -> HttpResponse:
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        product = form.save()
        return redirect('products:details', pk=product.pk, slug=product.slug)

    context = {
        'form': form,
    }
    return render(request, 'inventory/product-create-page.html', context)

