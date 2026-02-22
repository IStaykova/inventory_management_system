from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from inventory.models import Product
from orders.forms import OrderAddProductForm, OrderStatusForm
from orders.models import Order, OrderedProduct
from orders.services import cart

def order_list(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.all().order_by('created_at')
    return render(request, 'orders/order-list-page.html', {'orders': orders})

def order_details(request: HttpRequest, order_number) -> HttpResponse:
    order = get_object_or_404(Order, order_number=order_number)
    product = (OrderedProduct.objects.filter(order=order).select_related('product'))
    total_price = 0
    for p in product:
     p.line_total = p.quantity * p.unit_price
     total_price += p.line_total

    return render(request, 'orders/order-details-page.html',
            {'order': order,
                   'product': product,
                   'total_price': total_price})

def order_status(request: HttpRequest, order_number) -> HttpResponse:
    order = get_object_or_404(Order, order_number=order_number)

    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("orders:details", order_number=order_number)
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'orders/order-status-page.html', {'order': order, 'form': form})

def order_delete(request: HttpRequest, order_number):
    order = get_object_or_404(Order, order_number=order_number)
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

def order_edit(request: HttpRequest, order_number) -> HttpResponse:
    order = get_object_or_404(Order, order_number=order_number)
    items = OrderedProduct.objects.filter(order=order).select_related('product')
    add_form = OrderAddProductForm()
    return render(request, 'orders/order-edit-page.html', {'order': order, 'items': items, 'add_form': add_form})

def order_add_item(request, order_number) -> HttpResponse:
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == "POST":
        form = OrderAddProductForm(request.POST)
        if form.is_valid():
            try:
                cart.add_cart_item(order, form.cleaned_data['product'], form.cleaned_data['quantity'])
            except cart.CartError as e:
                messages.error(request, str(e))

    return redirect('orders:edit', order_number=order.order_number)

def order_inc_item_qty(request, order_number, product_id) -> HttpResponse:
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == "POST":
        try:
            cart.increase_item_qty(order, product_id)
        except cart.CartError as e:
            list(messages.get_messages(request))
            messages.error(request, str(e))

    return redirect('orders:edit', order_number=order.order_number)

def order_dec_item_qty(request, order_number, product_id) -> HttpResponse:
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == "POST":
        try:
            cart.decrease_item_qty(order, product_id)
            if not OrderedProduct.objects.filter(order=order).exists():
                order.delete()
                return redirect('orders:order_list')
        except cart.CartError as e:
            messages.error(request, str(e))

    return redirect('orders:edit', order_number=order.order_number)

def order_remove_item(request, order_number, product_id) -> HttpResponse:
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == "POST":
        try:
            cart.remove_cart_item(order, product_id)
            if not OrderedProduct.objects.filter(order=order).exists():
                order.delete()
                return redirect('orders:order_list')
        except cart.CartError as e:
            messages.error(request, str(e))

    return redirect('orders:edit', order_number=order.order_number)







