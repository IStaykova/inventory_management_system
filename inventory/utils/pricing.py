from decimal import Decimal

from inventory.models import Product


def apply_sale_price(product: Product, prev_price: Decimal | None):
    if prev_price is None:
        return
    if product.price < prev_price:
        product.old_price = prev_price
    else:
        product.old_price = None