from django.db.models.aggregates import Sum

from orders.models import Order, OrderedProduct

def cart_counter(request):
    cart_count = 0
    order = Order.objects.filter(status=Order.Status.NEW).first()

    if order:
        cart_count = (OrderedProduct.objects.filter(order=order).aggregate(total=Sum('quantity'))['total'] or 0)

    return {'cart_count': cart_count,
            'cart_order': order}