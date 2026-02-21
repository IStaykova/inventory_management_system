from django.urls import path

from reviews.views import product_reviews, review_create, review_edit, review_delete, top_products

app_name = "reviews"

urlpatterns = [
    path('product/<int:product_id>/', product_reviews, name='product_reviews'),
    path('product/<int:product_id>/add', review_create, name='review_create'),
    path('edit/<int:pk>/', review_edit, name='review_edit'),
    path('delete/<int:pk>/', review_delete, name='review_delete'),
    path('top/', top_products, name='top_products'),
]