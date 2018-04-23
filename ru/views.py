from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'ru/index.html')


def contacts(request):
    return render(request, 'ru/contacts.html')


def payments(request):
    return render(request, 'ru/payments.html')