from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from orders.models import Order


def order_list(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.all()
    return render(request, 'orders/order-list-page.html', {'orders': orders})

def order_details(request: HttpRequest, pk) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order-details-page.html', {'order': order})

def order_status(request: HttpRequest, pk) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order-status-page.html', {'order': order})

def order_edit(request: HttpRequest, pk) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order-edit-page.html', {'order': order})

def order_delete(request: HttpRequest, pk) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order-delete-page.html', {'order': order})
