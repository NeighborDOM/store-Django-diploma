from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from products.models import Product, ProductCategory, Basket
from common.views import TitleMixin


# Create your views here.

class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = "DOM's Store"

    # def get_context_data(self, **kwargs):
    # context = super(IndexView, self).get_context_data()
    # context['title'] = "DOM's Store"
    # return context


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = "DOM's Store - Каталог"

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_pk = self.kwargs.get('category_pk')
        return queryset.filter(category_id=category_pk) if category_pk else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, pk):
    product = Product.objects.get(id=pk)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
