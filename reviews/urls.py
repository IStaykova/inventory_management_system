from django.urls import path

from reviews.views import ReviewCreateView, ReviewEditView, ReviewDeleteView, \
    TopReviewsListView, ProductReviewListView

app_name = "reviews"

urlpatterns = [
    path('product/<int:product_id>/', ProductReviewListView.as_view(), name='product_reviews'),
    path('product/<int:product_id>/add', ReviewCreateView.as_view(), name='review_create'),
    path('edit/<int:pk>/', ReviewEditView.as_view(), name='review_edit'),
    path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),
    path('top/', TopReviewsListView.as_view(), name='top_products'),
]