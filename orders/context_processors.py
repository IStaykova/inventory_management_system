from orders.services import cart

def cart_data(request):
    return cart.get_cart(request)