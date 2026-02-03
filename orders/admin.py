from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name')
    ordering = ('-created_at',)

    
