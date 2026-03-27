from django.urls import path, include
from orders.views import OrderListView, CartDetailView, CartItemIncreaseView, AddToCartView, \
    CartItemDecreaseView, \
    CartItemRemoveView, OrderCreateView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('list/', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='create'),

    path('cart/', CartDetailView.as_view(), name='cart'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_item'),
    path('cart/inc/<int:product_id>/', CartItemIncreaseView.as_view(), name='inc_item'),
    path('cart/dec/<int:product_id>/', CartItemDecreaseView.as_view(), name='dec_item'),
    path('cart/remove/<int:product_id>/', CartItemRemoveView.as_view(), name='remove_item'),

    path('<uuid:order_number>/', include([
        path('details', OrderDetailView.as_view(), name='order_details')
        # path('status/', order_status, name='status'),
        # path('edit/', order_edit, name='edit'),
        # path('delete/', order_delete, name='delete'),

    ])),

    ]

