from django.urls import path, include
from inventory.views import ProductCreateView, ProductEditView, ProductDetailView, ProductDeleteView, ProductListView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('details/<slug:slug>/', ProductDetailView.as_view(), name='details'),

    path('<int:pk>/', include([
        path('edit/', ProductEditView.as_view(), name='edit'),
        path('delete/', ProductDeleteView.as_view(), name='delete'),
    ])),
]