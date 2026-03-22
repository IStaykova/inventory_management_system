from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from inventory.forms import ProductForm, SearchForm
from inventory.mixins import StaffRequiredMixin
from inventory.models import Product
from inventory.utils.pricing import apply_sale_price

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()

        if 'searched_name' in self.request.GET:
            queryset = queryset.filter(name__icontains=self.request.GET.get('searched_name'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return  context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory/product-details-page.html'

class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product-create-page.html'

    def get_success_url(self):
        return reverse('products:details', kwargs={'slug': self.object.slug})

class ProductEditView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product-edit-page.html'

    def form_valid(self, form):
        prev_price = self.get_object().price
        apply_sale_price(form.instance, prev_price)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products:details', kwargs={'slug': self.object.slug})

class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:home')




