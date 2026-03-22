from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from inventory.models import Product

UserModel = get_user_model()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(validators=[MinLengthValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product} - {self.rating}/5 by {self.author}'
