from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from .models import Products, Category, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm


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


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('ru:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    return redirect('ru:cart_detail')


def cart_detail(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
    return render(request, 'ru/cart_detail.html', {
        'category_list': category_list,
        'products_list': products_list,
        'cart': cart
    })


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'ru/orders/order_created.html', {'order': order})

    form = OrderCreateForm()
    return render(request, 'ru/orders/order_create.html', {'cart': cart,
                                                           'form': form})


def product_detail(request, slug):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    cart_product_form = CartAddProductForm()
    product = get_object_or_404(Products, slug=slug, available=True)
    return render(request, 'ru/product_detail.html', {
        'category_list': category_list,
        'products_list': products_list,
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
