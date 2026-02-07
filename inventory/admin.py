from django.contrib import admin

from inventory.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'category', 'slug')
    search_fields = ('name',)
    list_filter = ('category',)
