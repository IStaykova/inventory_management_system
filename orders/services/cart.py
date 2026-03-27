from decimal import Decimal

from django.shortcuts import get_object_or_404

from inventory.models import Product

class CartError(Exception):
    pass

CART_SESSION_KEY = 'cart'

def _get_raw_cart(request) -> dict:
    return request.session.get(CART_SESSION_KEY, {})

def _save_cart(request, cart: dict) -> None:
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def get_cart(request) -> dict:
    raw_cart = _get_raw_cart(request)

    product_ids = raw_cart.keys()
    products = Product.objects.filter(pk__in=product_ids)

    items = []
    total_price = Decimal('0.00')
    total_quantity = 0

    products_map = {str(product.pk): product for product in products}

    for product_id, item_data in raw_cart.items():
        product = products_map.get(str(product_id))
        if product is None:
            continue

        quantity = int(item_data['quantity'])
        unit_price = Decimal(item_data['unit_price'])
        line_total = unit_price * quantity

        items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'line_total': line_total,
        })

        total_price += line_total
        total_quantity += quantity

    return {
        'items': items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    }

def add_cart_item(request, product_id:int, quantity: int = 1) -> None:
    if quantity <= 0:
        raise CartError("Quantity must be а positive number!")

    product = get_object_or_404(Product, pk=product_id)
    cart = _get_raw_cart(request)
    key = str(product.pk)
    current_qty = cart.get(key, {}).get('quantity', 0)
    new_qty = current_qty + quantity

    if new_qty > product.stock_quantity:
        raise CartError("Not enough quantity in stock!")

    cart[key] = {
        'quantity': new_qty,
        'unit_price': str(product.price),
    }
    _save_cart(request, cart)

def increase_item_qty(request, product_id:int) -> None:
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_raw_cart(request)
    key = str(product.pk)

    if key not in cart:
        raise CartError('Item is not in the cart.')

    new_qty = cart[key]['quantity'] + 1

    if new_qty > product.stock_quantity:
        raise CartError('Not enough quantity in stock!')

    cart[key]['quantity'] = new_qty
    _save_cart(request, cart)

def decrease_item_qty(request, product_id:int) -> None:
    cart = _get_raw_cart(request)
    key = str(product_id)

    if key not in cart:
        raise CartError('Item is not in the cart.')

    if cart[key]['quantity'] <= 1:
        del cart[key]
    else:
        cart[key]['quantity'] -= 1

    _save_cart(request, cart)

def remove_cart_item(request, product_id:int) -> None:
    cart = _get_raw_cart(request)
    key = str(product_id)

    if key in cart:
        del cart[key]
        _save_cart(request, cart)

def clear_cart(request) -> None:
    request.session.pop(CART_SESSION_KEY, None)
    request.session.modified = True