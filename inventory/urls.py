from django.urls import path

from inventory.views import index

app_name = 'inventory'

urlpatterns = [
    path('', index, name='index')
]