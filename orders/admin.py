from django.contrib import admin

from accounts.models import Address
from orders.models import Order, OrderedProduct

admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(Address)

    
