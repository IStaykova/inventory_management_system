from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views import View

from inventory.models import Product
from orders.forms import OrderAddProductForm, OrderStatusForm
from orders.mixins import StaffRequiredMixin
from orders.models import Order, OrderedProduct
from orders.services import cart

class OrderListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order-list-page.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return (
            Order.objects
            .exclude(status=Order.Status.CART)
            .select_related('customer_name')
            .order_by('created_at')
        )

class CartDetailView(TemplateView):
    template_name = 'orders/cart-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_data = cart.get_cart(self.request)
        context['items'] = cart_data['items']
        context['total_price'] = cart_data['total_price']
        context['total_quantity'] = cart_data['total_quantity']
        return context

class AddToCartView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            cart.add_cart_item(request, product_id=pk, quantity=1)
        except cart.CartError as e:
            messages.error(request, str(e))

        return redirect(request.META.get('HTTP_REFERER', '/'))

class CartItemIncreaseView(View):
    def post(self, request, product_id, *args, **kwargs):
        try:
            cart.increase_item_qty(request, product_id=product_id)
        except cart.CartError as e:
            messages.error(request, str(e))

        return redirect('orders:cart')

class CartItemDecreaseView(View):
    def post(self, request, product_id, *args, **kwargs):
        try:
            cart.decrease_item_qty(request, product_id=product_id)
            cart_data = cart.get_cart(request)
            if not cart_data['items']:
                messages.info(request, 'Cart is empty!')
        except cart.CartError as e:
            messages.error(request, str(e))

        return redirect('orders:cart')

class CartItemRemoveView(View):
    def post(self, request, product_id, *args, **kwargs):
        try:
            cart.remove_cart_item(request, product_id=product_id)
            cart_data = cart.get_cart(request)
            if not cart_data['items']:
                messages.info(request, 'Cart is empty!')
        except cart.CartError as e:
            messages.error(request, str(e))

        return redirect('orders:cart')

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_data = cart.get_cart(request)

        if not cart_data['items']:
            messages.error(request, 'Your cart is empty.')
            return redirect('orders:cart')

        return redirect('orders:create_order')

class CreateOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order-create-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_data = cart.get_cart(self.request)
        context['items'] = cart_data['items']
        context['total_price'] = cart_data['total_price']
        return context

    def post(self, request, *args, **kwargs):
        order = checkout.create_order_from_cart(request)
        return redirect('orders:details', order_number=order.order_number)




# def order_status(request: HttpRequest, order_number) -> HttpResponse:
#     order = get_object_or_404(Order, order_number=order_number)
#
#     if request.method == "POST":
#         form = OrderStatusForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect("orders:details", order_number=order_number)
#     else:
#         form = OrderStatusForm(instance=order)
#
#     return render(request, 'orders/order-status-page.html', {'order': order, 'form': form})
#
# def order_delete(request: HttpRequest, order_number):
#     order = get_object_or_404(Order, order_number=order_number)
#     if request.method == "POST":
#         order.delete()
#         return redirect("orders:order_list")
#

# def order_edit(request: HttpRequest, order_number) -> HttpResponse:
#     order = get_object_or_404(Order, order_number=order_number)
#     items = OrderedProduct.objects.filter(order=order).select_related('product')
#     add_form = OrderAddProductForm()
#     return render(request, 'orders/order-edit-page.html', {'order': order, 'items': items, 'add_form': add_form})
#
