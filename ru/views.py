from decimal import Decimal
from .tasks import order_created
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from paypal.standard.forms import PayPalPaymentsForm
from .models import Products, Category, OrderItem, Order, Comments, Contact, Payment
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, UserForm, ProfileForm, CommentCreateForm, SupportForm
from django.contrib.admin.views.decorators import staff_member_required

"""
from weasyprint import HTML, CSS        
from main import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
"""


# Create your views here.

def support(request):
    current_user = request.user
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            sup = form.save()
            return render(request, 'ru/supports/support_successful.html', {'sup': sup})
    try:
        form = SupportForm(initial={
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'number_phone': current_user.profile.number_phone,
        })
        return render(request, 'ru/supports/support.html', {'form': form})
    except:
        form = SupportForm()
        return render(request, 'ru/supports/support.html', {'form': form})


def contact(request):
    contacts = Contact.objects.all()
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    return render(request, 'ru/contact.html', {
        'category_list': category_list,
        'products_list': products_list,
        'contacts': contacts
    })


def payment(request):
    payments = Payment.objects.all()
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    return render(request, 'ru/payment.html', {
        'category_list': category_list,
        'products_list': products_list,
        'payments': payments
    })


@login_required
@transaction.atomic
def my_room(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    order_list = Order.objects.all()
    current_user = str(request.user)
    user = User.objects.get(username=current_user)
    order = Order.objects.get(id=user.id)
    order_item = OrderItem.objects.get(id=order.id)

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('ru:my_room')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'ru/my_room.html', {
        'category_list': category_list,
        'products_list': products_list,
        'order_list': order_list,
        'order': order,
        'order_item': order_item,
        'user_form': user_form,
        'profile_form': profile_form,
        'cart': cart,
        'user':user
    })


def comment_add(request, product_id):
    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_product = Products.objects.get(id=product_id)
            comment.author = request.user
            form.save()
            return redirect('ru:category_list')


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
        if form.is_valid() and cart:
            order = form.save()
            for item in cart:
                if item['discount']:
                    item['price'] = item['discount_price']
                    OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                else:
                    OrderItem.objects.create(order=order, product=item['product'],
                                             discount=item['discount'],
                                             price=item['price'],
                                             quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('ru:process'))
    try:
        if request.user.is_anonymous:
            current_user = 1
            form = OrderCreateForm(initial={
                'user': current_user
            })
        else:
            current_user = request.user
            form = OrderCreateForm(initial={
                'user': current_user,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'address': current_user.profile.address,
                'postal_code': current_user.profile.postal_code,
                'city': current_user.profile.city,
            })
        return render(request, 'ru/orders/order_create.html', {'cart': cart, 'form': form})
    except:
        form = OrderCreateForm()

        return render(request, 'ru/orders/order_create.html', {'cart': cart,
                                                               'form': form})


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
        'item_name': 'Заказ {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'UAH',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('ru:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('ru:canceled'))
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'ru/payment/process.html', {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'ru/payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'ru/payment/canceled.html')


def shares_list_view(request):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    paginator = Paginator(products_list, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)
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
        'products': products
    })


# CSV order print
@staff_member_required
def admin_order_detail(request, order_id):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/ru/orders/detail.html', {
        'cart': cart,
        'order': order
    })


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
    paginator = Paginator(products_list, 3)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
    return render(request, 'ru/category_list.html', {
        'category_list': category_list,
        'products_list': products_list,
        'cart': cart,
        'products': products
    })


def category_detail_view(request, slug):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    category = get_object_or_404(Category, slug=slug, available=True)
    paginator = Paginator(products_list, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'ru/category_detail.html', {
        'category_list': category_list,
        'products_list': products_list,
        'category': category,
        'products': products
    })


def product_detail_view(request, slug):
    category_list = Category.objects.all()
    products_list = Products.objects.all()
    comments_list = Comments.objects.all()
    cart_product_form = CartAddProductForm()
    product = get_object_or_404(Products, slug=slug, available=True)
    comment_product_form = CommentCreateForm(initial={})
    return render(request, 'ru/product_detail.html', {
        'category_list': category_list,
        'products_list': products_list,
        'product': product,
        'comments_list': comments_list,
        'cart_product_form': cart_product_form,
        'comment_product_form': comment_product_form
        })




