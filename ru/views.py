from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Products


# Create your views here.

def contact(request):
    return render(request, 'ru/contact.html')


def payment(request):
    return render(request, 'ru/payment.html')


class ProductsListView(ListView):
    model = Products

