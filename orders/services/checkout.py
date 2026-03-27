from django.db import transaction

from orders.models import Order, OrderedProduct
from orders.services.cart import clear_cart, get_cart

class CreateOrderError(Exception):
    pass

@transaction.atomic
def create_order(*, request, cleaned_data):
    cart_data = get_cart(request)

    if not cart_data['items']:
        raise CreateOrderError('Your cart is empty.')

    order = Order.objects.create(
        user=request.user,
        first_name=cleaned_data['first_name'],
        last_name=cleaned_data['last_name'],
        phone_number=cleaned_data['phone_number'],
        email=cleaned_data['email'],
        shipping_address=cleaned_data['shipping_address'],
        amount_paid=cart_data['total_price'],
    )

    for item in cart_data['items']:
        product = item['product']

        OrderedProduct.objects.create(
            order=order,
            user=request.user,
            product=product,
            quantity=item['quantity'],
            price=item['unit_price'],
        )

        product.stock_quantity -= item['quantity']
        product.save(update_fields=['stock_quantity'])

    clear_cart(request)
    return order