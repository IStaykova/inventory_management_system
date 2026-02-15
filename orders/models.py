import uuid

from django.db import models

class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELED = 'CANCELED', 'Canceled'

    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return f"Order {self.order_number} for {self.customer_name}"

class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE, related_name="order_products")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product} for Order {self.order.order_number}"