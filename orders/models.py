
from django.db import models
from django.utils.timezone import localdate


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELED = 'CANCELED', 'Canceled'


    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)

    def save(self, *args, **kwargs):
        if not self.order_number:
            year = localdate().year
            last_id = Order.objects.count() + 1
            self.order_number = f"ORD-{year}-{last_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} for {self.customer_name}"