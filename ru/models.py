from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, help_text='Нужно использовать для создания "хороших" URL-ов')
    available = models.BooleanField(default=True, verbose_name="Отображать")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ru:category_detail', args={self.slug})


class Products(models.Model):
    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=50, db_index=True, verbose_name="")
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, help_text='Нужно использовать для создания "хороших" URL-ов')
    category = models.ForeignKey(Category, db_index=True, on_delete=models.CASCADE, related_name="rel_category",
                                 verbose_name="Категория продукта")
    image = models.ImageField(upload_to='products/img/%Y/%m/%d/', blank=True,
                              verbose_name="Картинка для новостей (300 x 300)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена(грн)")
    short_description = models.TextField(blank=True, verbose_name="Короткое описание в листе")
    description = RichTextUploadingField(blank=True, verbose_name="Детальное описание")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    available = models.BooleanField(default=True, verbose_name="Отображать")
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, verbose_name='В процентах')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ru:product_detail', args={self.slug})

    def get_discount(self):
        price = Decimal(self.price-(self.price*self.discount/100))
        return price


class Order(models.Model):

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(verbose_name='Адрес', max_length=250)
    postal_code = models.CharField(verbose_name='Почтовый код', max_length=20)
    city = models.CharField(verbose_name='Город', max_length=100)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(100)])

    def __str__(self):
        return 'Заказ: {}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
