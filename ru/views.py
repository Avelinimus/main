from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Products, Category


# Create your views here.

def contact(request):
    return render(request, 'ru/contact.html')


def payment(request):
    return render(request, 'ru/payment.html')


def my_room(request):
    return render(request, 'ru/my_room.html')


class ProductsListView(ListView):
    model = Products
    context_object_name = "products_list"
    queryset = Products.objects.all()
    template_name = "ru/products_list.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category