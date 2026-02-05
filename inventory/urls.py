from django.urls import path, include
from inventory.views import home_page, product_details

app_name = 'products'
urlpatterns = [
    path('', home_page, name='home'),
    path('<int:pk>/', include([
        path('details/', product_details, name='details'),
    ])),
]