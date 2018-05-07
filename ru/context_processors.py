from .cart import Cart
from .models import Products, Category


def cart(request):
    return {'cart': Cart(request)}

