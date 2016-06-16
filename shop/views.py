from cart.forms import CartAddProductForm
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from shop.models import Product, Category


class ProductListView(ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    model = Product

    # Variaveis universais, acessivel a todas funcoes
    category = None

    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        products = qs.filter(available=True)

        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=self.category)

        return products

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
    model = Product

    def get_object(self, queryset=None):
        objeto = get_object_or_404(self.model, id=self.kwargs['id'], slug=self.kwargs['slug'], available=True)
        return objeto

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context
