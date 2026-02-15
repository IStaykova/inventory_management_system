from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from inventory.forms import ProductForm, SearchForm
from inventory.models import Product

def home_page(request: HttpRequest) -> HttpResponse:
    form = SearchForm(request.GET or None)
    products = Product.objects.all().order_by('name')

    if request.GET and form.is_valid():
        searched_product_name = form.cleaned_data['name']
        products = products.filter(name__icontains=searched_product_name)

    context = {
        "products": products,
        "form": form,
    }
    return render(request, 'inventory/product-list.html', context )

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

def product_edit(request: HttpRequest, pk:int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST" and form.is_valid():
        instance = form.save()
        return redirect('products:details', pk=product.pk, slug=instance.slug)

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'inventory/product-edit-page.html', context)

def product_delete(request: HttpRequest, pk:int) -> HttpResponse:
    Product.objects.get(pk=pk).delete()
    return redirect('products:home')






