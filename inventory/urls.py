from django.urls import path, include
from inventory.views import home_page, product_details, product_create, product_edit, product_delete

app_name = 'products'
urlpatterns = [
    path('', home_page, name='home'),
    path('create/', product_create, name='create'),
    path('<int:pk>/details/<slug:slug>/', product_details, name='details'),

    path('<int:pk>/', include([
        path('edit/', product_edit, name='edit'),
        path('delete/', product_delete, name='delete'),
    ])),
]