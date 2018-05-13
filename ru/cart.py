from decimal import Decimal
from django.conf import settings
from .models import Products


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Итерация по товарам

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['discount'] = Decimal(item['discount'])
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['discount_price'] = item['price']+(-item['price'] * item['discount']/100)
            item['total_discount_price'] = item['discount_price'] * item['quantity']
            yield item

    # Количество товаров
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'discount': str(product.discount)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_discount(self):
        return sum(Decimal(item['price']) * item['quantity'] * Decimal(item['discount'])/100 for item in self.cart.values())

    def get_total_price_with_discount(self):
        return self.get_total_price() - self.get_total_discount()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

