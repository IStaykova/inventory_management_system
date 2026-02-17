from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from inventory.models import Product
from orders.forms import OrderAddProductForm, OrderStatusForm
from orders.models import Order, OrderedProduct

def order_list(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.all().order_by('created_at')
    return render(request, 'orders/order-list-page.html', {'orders': orders})

def order_details(request: HttpRequest, pk) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)
    product = (OrderedProduct.objects.filter(order=order).select_related('product'))
    total_price = 0
    for p in product:
     p.line_total = p.quantity * p.unit_price
     total_price += p.line_total

    return render(request, 'orders/order-details-page.html',
            {'order': order,
                   'product': product,
                   'total_price': total_price})

def order_status(request: HttpRequest, pk) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("orders:details", pk=order.pk)
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'orders/order-status-page.html', {'order': order, 'form': form})

#TODO: Refactor this view to handle authorization
def order_edit(request: HttpRequest, pk) -> HttpResponse:
    # if order.status != Order.Status.NEW:
    #     return redirect("orders:details", pk=order.pk)
    order = get_object_or_404(Order, pk=pk)
    items = OrderedProduct.objects.filter(order=order).select_related('product')
    add_form = OrderAddProductForm()
    return render(request, 'orders/order-edit-page.html', {'order': order, 'items': items, 'add_form': add_form} )

def order_delete(request: HttpRequest, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("orders:order_list")

def order_create(request: HttpRequest, pk) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    if product.stock_quantity <= 0:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    order = (Order.objects.filter(status=Order.Status.NEW).order_by("-created_at").first())
    if order is None:
        order = Order.objects.create(customer_name="Guest")

    item, _ = OrderedProduct.objects.get_or_create(
        order=order,
        product=product,
        defaults={"quantity": 0, "unit_price": product.price},
    )
    item.quantity += 1
    item.save()

    product.stock_quantity -= 1
    product.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

