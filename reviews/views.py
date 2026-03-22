from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.aggregates import Avg
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from inventory.models import Product
from reviews.forms import ReviewForm
from reviews.models import Review

class ProductReviewListView(ListView):
    model = Review
    template_name = 'reviews/product-reviews-page.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        context['avg_rating'] = context['reviews'].aggregate(avg=Avg('rating'))['avg']

        return context

class TopReviewsListView(ListView):
    model = Product
    template_name = 'reviews/top-product-page.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return (
            Product.objects
            .annotate(avg_rating=Avg('reviews__rating'))
            .exclude(avg_rating=None)
            .order_by('-avg_rating')
        )

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review-form-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        return context

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs['product_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('reviews:product_reviews', kwargs={'product_id':self.kwargs['product_id']})

class ReviewEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review-form-page.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

    def get_success_url(self):
        return reverse('reviews:product_reviews',kwargs={'product_id': self.object.product_id}
        )

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review-delete-page.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse(
            'reviews:product_reviews',
            kwargs={'product_id': self.object.product_id}
        )

