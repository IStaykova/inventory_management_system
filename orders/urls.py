from django.urls import path, include
from orders.views import order_list, order_details, order_status, order_edit, order_delete, order_create

app_name = 'orders'

urlpatterns = [
    path('list/', order_list, name='order_list'),
    path('<int:pk>/', include([
        path('details/', order_details, name='details'),
        path('status/', order_status, name='status'),
        path('edit/', order_edit, name='edit'),
        path('delete/', order_delete, name='delete'),
        path('create/', order_create, name='create')
    ])),

    ]

