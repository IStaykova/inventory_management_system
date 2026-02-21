from django.urls import path, include
from orders.views import order_list, order_details, order_status, order_edit, order_delete, order_create, \
    order_add_item, order_inc_item_qty, order_dec_item_qty, order_remove_item

app_name = 'orders'

urlpatterns = [
    path('list/', order_list, name='order_list'),
    path('<int:pk>/create', order_create, name='create'),

    path('<uuid:order_number>/', include([
        path('details/', order_details, name='details'),
        path('status/', order_status, name='status'),
        path('edit/', order_edit, name='edit'),
        path('delete/', order_delete, name='delete'),

        path('add-item/', order_add_item, name='add_item'),
        path('inc/<int:product_id>/', order_inc_item_qty, name='inc'),
        path('dec/<int:product_id>/', order_dec_item_qty, name='dec'),
        path('remove/<int:product_id>/', order_remove_item, name='remove_item'),
    ])),

    ]

