from django.urls import path
from inventory.views import home_page

app_name = 'inventory'
urlpatterns = [
    path('', home_page, name='home')
]