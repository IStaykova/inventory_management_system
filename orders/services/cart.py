from django.db import transaction

from inventory.models import Product
from orders.models import Order, OrderedProduct

class CartError(Exception):
    pass

def is_cart_editable(order: Order):
    if order.status != Order.Status.NEW:
        raise CartError("You can no longer edit this order!")

@transaction.atomic
def add_cart_item(order: Order, product: Product, quantity: int) -> None:
    is_cart_editable(order)
    product = Product.objects.select_for_update().get(pk=product.pk)
    if quantity <= 0:
        raise CartError("Quantity must be positive number!")
    if product.stock_quantity < quantity:
        raise CartError("Not enough quantity in stock!")

    item, _ = OrderedProduct.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 0, 'unit_price': product.price},
    )
    item.quantity += quantity
    if not item.unit_price:
        item.unit_price = product.price
    item.save()

    product.stock_quantity -= quantity
    product.save()

@transaction.atomic
def increase_item_qty(order: Order, product_id: int) -> None:
    is_cart_editable(order)
    product = Product.objects.select_for_update().get(pk=product_id)
    if product.stock_quantity <= 0:
        raise CartError('Not enough quantity in stock!')

    item, _ = OrderedProduct.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 0, 'unit_price': product.price},
    )
    item.quantity += 1
    item.save()

    product.stock_quantity -= 1
    product.save()

@transaction.atomic
def decrease_item_qty(order: Order, product_id: int) -> None:
    is_cart_editable(order)
    item = (
        OrderedProduct.objects.select_for_update()
        .select_related('product')
        .filter(order=order, product_id=product_id)
        .first()
    )
    if not item:
        return
    item.product.stock_quantity +=1
    item.product.save()

    if item.quantity <= 1:
        item.delete()
    else:
        item.quantity -= 1
        item.save()

@transaction.atomic
def remove_cart_item(order: Order, product_id: int) -> None:
    is_cart_editable(order)
    item = (
        OrderedProduct.objects.select_for_update()
        .select_related('product')
        .filter(order=order, product_id=product_id)
        .first()
    )
    if not item:
        return
    item.product.stock_quantity += item.quantity
    item.product.save()
    item.delete()
