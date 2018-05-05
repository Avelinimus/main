from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.generic import ListView, DetailView

from cart.forms import CartAddProductForm
from .models import Products, Category


# Create your views here.

def contact(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    return render(request, 'ru/contact.html', {
        'category_list': category_list,
        'products_list': products_list,
    })


def payment(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    return render(request, 'ru/payment.html', {
        'category_list': category_list,
        'products_list': products_list,
    })


def my_room(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    return render(request, 'ru/my_room.html', {
        'category_list': category_list,
        'products_list': products_list,
    })


def product_detail(request, id, slug):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    product = get_object_or_404(Products, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'ru/product_detail.html', {
        'products_list': products_list,
        'category_list': category_list,
        'product': product,
        'cart_product_form': cart_product_form
    })


class CategoryListView(ListView):
    context_object_name = "category_list"
    queryset = Category.objects.all()
    template_name = "ru/category_list.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['products_list'] = Products.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "ru/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['products_list'] = Products.objects.all()
        return context
