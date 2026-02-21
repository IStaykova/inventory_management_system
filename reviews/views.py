from django.db.models.aggregates import Avg
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from inventory.models import Product
from reviews.forms import ReviewForm
from reviews.models import Review

def product_reviews(request: HttpRequest, product_id:int) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    return render(request, 'reviews/product-reviews-page.html', {
                'product':product,
                'reviews': reviews,
                'avg_rating': avg_rating,
            })

def review_create(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST or None)

    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.save()
        return redirect('reviews:product_reviews', product_id=product.pk)

    return render(request, 'reviews/review-form-page.html', {
            'product': product,
            'form': form,
        })

def review_edit(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review, pk=pk)
    form = ReviewForm(request.POST or None, instance=review)

    if form.is_valid():
        form.save()
        return redirect('reviews:product_reviews', product_id=review.product_id)

    return render(request, 'reviews/review-form-page.html', {
            'product': review.product,
            'form': form,
        })

def review_delete(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review, pk=pk)

    if request.method == "POST":
        product_id = review.product_id
        review.delete()
        return redirect('reviews:product_reviews', product_id=product_id)

    return render(request, 'reviews/review-delete-page.html', {'review': review})

def top_products(request: HttpRequest) -> HttpResponse:
    products = (
        Product.objects
        .annotate(avg_rating=Avg('reviews__rating'))
        .exclude(avg_rating=None)
        .order_by('-avg_rating')[:5]
    )
    return render(request, 'reviews/top-product-page.html', {'products': products})
