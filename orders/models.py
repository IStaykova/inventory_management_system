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