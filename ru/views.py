from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from .models import Products, Category, OrderItem, Order
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from django.contrib.admin.views.decorators import staff_member_required

"""
from weasyprint import HTML, CSS
from main import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
"""


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
                if item['discount']:
                    item['price'] = item['discount_price']
                    OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                else:
                    OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])

            cart.clear()
            return render(request, 'ru/orders/order_created.html', {'order': order})
    form = OrderCreateForm()
    return render(request, 'ru/orders/order_create.html', {'cart': cart,
                                                           'form': form})


def shares_list_view(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
    return render(request, 'ru/shares.html', {
        'category_list': category_list,
        'products_list': products_list,
        'cart': cart,
    })


# CSV order print
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/ru/orders/detail.html', {'order': order})


"""
# PDF order print
@staff_member_required
def admin_order_PDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('ru/orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    HTML(string=html).write_pdf(response,
                                stylesheets=[CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])
    return response
"""


def category_list_view(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
    return render(request, 'ru/category_list.html', {
        'category_list': category_list,
        'products_list': products_list,
        'cart': cart
    })


def category_detail_view(request, slug):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    category = get_object_or_404(Category, slug=slug, available=True)
    return render(request, 'ru/category_detail.html', {
        'category_list': category_list,
        'products_list': products_list,
        'category': category,
    })


def product_detail_view(request, slug):
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
