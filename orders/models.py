import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from inventory.models import Product

UserModel = get_user_model()

class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELED = 'CANCELED', 'Canceled'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=5000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.first_name} {self.last_name}"


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_products')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ordered {self.quantity} x {self.product.name} for Order {self.order.id}"