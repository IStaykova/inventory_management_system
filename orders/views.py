from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, UpdateView, DetailView
from django.views import View

from accounts.models import Address
from inventory.models import Product
from orders.forms import OrderCreateForm, OrderStatusForm
from orders.mixins import StaffRequiredMixin
from orders.models import Order, OrderedProduct
from orders.services import cart
from orders.services.cart import get_cart
from orders.services.checkout import CreateOrderError, create_order
from inventory_management_system import settings
from inventory_management_system.services.emails import send_template_email

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order-list-page.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = Order.objects.select_related('user').order_by('date_ordered')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

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

class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = 'orders/order-create-page.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('products:home')

    def get_initial(self):
        initial = super().get_initial()
        profile = self.request.user.profile

        initial['first_name'] = profile.first_name
        initial['last_name'] = profile.last_name
        initial['phone_number'] = profile.phone_number
        initial['email'] = self.request.user.email

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_data'] = get_cart(self.request)
        return context

    def form_valid(self, form):
        try:
            order = create_order(
                request=self.request,
                cleaned_data=form.cleaned_data,
            )
            send_template_email(
                to_email=self.request.user.email,
                template_id=settings.SENDGRID_ORDER_CONFIRMATION_TEMPLATE,
                dynamic_data={
                    "name": self.request.user.username,
                    "products": [
                        {
                            "name": item.product.name,
                            "quantity": item.quantity,
                            "price": str(item.price),
                        }
                        for item in order.ordered_products.all()
                    ],
                    "total_price": str(order.amount_paid),
                },
            )

        except CreateOrderError as e:
            messages.error(self.request, str(e))
            return redirect('orders:create')

        messages.success(
            self.request,
            'Your order has been placed successfully! You will receive details by email',
        )
        return super().form_valid(form)

class OrderStatusUpdateView(StaffRequiredMixin, UpdateView):
    model = Order
    form_class = OrderStatusForm
    template_name = 'orders/order-status-page.html'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def form_valid(self, form):
        messages.success(self.request, "Order status updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('orders:order_list')

class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orders/order-details-page.html'
    model = Order
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def get_queryset(self):
        return (
            Order.objects
            .select_related('user')
            .prefetch_related(
                Prefetch(
                    'ordered_products',
                    queryset=OrderedProduct.objects.select_related('product'),
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordered_products = self.object.ordered_products.all()

        for item in ordered_products:
            item.item_total = item.price * item.quantity

        total_order_price = sum(item.item_total for item in ordered_products)

        context['ordered_products'] = ordered_products
        context['total_order_price'] = total_order_price
        return context
