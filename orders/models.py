import uuid
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

UserModel = get_user_model()

class Order(models.Model):
    class Status(models.TextChoices):
        CART = 'CART', 'Cart'
        NEW = 'NEW', 'New'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELED = 'CANCELED', 'Canceled'

    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer_name = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.CART)

    def __str__(self):
        return f"Order {self.order_number} for {self.customer_name}"

class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE, related_name="ordered_products")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product} for Order {self.order.order_number}"