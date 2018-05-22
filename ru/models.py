from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    name = models.CharField(max_length=50, db_index=True, verbose_name="Название продукта")
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, help_text='Нужно использовать для создания "хороших" URL-ов')
    category = models.ForeignKey(Category, db_index=True, on_delete=models.CASCADE, related_name="rel_category",
                                 verbose_name="Категория продукта")
    image = models.ImageField(upload_to='products/img/%Y/%m/%d/', blank=True,
                              verbose_name="Картинка для новостей (300 x 300)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена(грн)")
    short_description = models.TextField(max_length=200, blank=True, verbose_name="Короткое описание в листе(150)")
    description = RichTextUploadingField(blank=True, verbose_name="Детальное описание")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    available = models.BooleanField(default=True, verbose_name="Отображать")
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0,
                                   verbose_name='Скидка (в процентах)')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ru:product_detail', args={self.slug})

    def get_discount(self):
        price = Decimal(self.price - (self.price * self.discount / 100))
        return price


class Order(models.Model):

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(verbose_name='Адрес', max_length=250)
    postal_code = models.CharField(verbose_name='Почтовый код', max_length=20)
    city = models.CharField(verbose_name='Город', max_length=100)
    number_phone = models.CharField(verbose_name='Мобильный телефон(обязательное поле)', max_length=13, default='+380', validators=[MinLengthValidator(13)])
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)
    sent = models.BooleanField(verbose_name='Товар отправлен', default=False)

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def get_total_cost(self):
        cost = Decimal(sum(item.get_cost() for item in self.items.all()))
        return cost

    def get_absolute_url(self):
        return reverse('ru:my_room_order_detail', args={self.id})


class OrderItem(models.Model):

    class Meta:
        ordering = ['order']
        verbose_name = 'Заказаный предмет'
        verbose_name_plural = 'Заказанные предметы'

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(100)])

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        if self.discount > 0:
            return ((self.discount/100) * self.price) * self.quantity
        else:
            return self.price * self.quantity


class Comments(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    title = models.CharField(max_length=120, verbose_name='Оглавление')
    comments_product = models.ForeignKey(Products, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    comments_text = models.TextField(verbose_name='Коментарий')
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    verified = models.BooleanField(default=False, verbose_name='Проверено')


class Profile(models.Model):

    class Meta:
        ordering = ['-user']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(verbose_name='Город', max_length=100, blank=True)
    address = models.CharField(verbose_name='Адрес', max_length=250, blank=True)
    postal_code = models.CharField(verbose_name='Почтовый код', max_length=20, blank=True)
    number_phone = models.CharField(verbose_name='Моб. телефон', max_length=13, default='+380', blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='День рождения')

    def __str__(self):
        return 'Профиль: {}'.format(self.user)

    @property
    def get_id_profile(self):
        return User.objects.get(pk=self.user_id)


class Support(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name = 'Оповещение о проблеме'
        verbose_name_plural = 'Оповещение о проблемах'

    title = models.CharField(max_length=150, verbose_name='Заголовок')
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    number_phone = models.CharField(verbose_name='Моб. телефон', max_length=13, default='+380', blank=True)
    description = RichTextUploadingField(verbose_name='Детальное описание проблемы')
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    verified = models.BooleanField(default=False, verbose_name='Проверено')


class Contact(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name = 'Описание для контактов'
        verbose_name_plural = 'Описание для контактов'

    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    description = RichTextUploadingField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title


class Payment(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name = 'Описание для доставки и оплаты'
        verbose_name_plural = 'Описание для доставки и оплаты'

    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    description = RichTextUploadingField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


