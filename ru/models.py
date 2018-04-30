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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ru:category_detail', args={self.slug})


class Products(models.Model):

    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок новости")
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, help_text='Нужно использовать для создания "хороших" URL-ов')
    category = models.ManyToManyField(Category,db_index=True, verbose_name="Категория продукта")
    image = models.ImageField(upload_to='products/img/%Y/%m/%d/', blank=True,
                              verbose_name="Картинка для новостей (300 x 300)")
    short_description = models.TextField(blank=True, verbose_name="Короткое описание в листе")
    description = RichTextUploadingField(blank=True, verbose_name="Детальное описание")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    available = models.BooleanField(default=True, verbose_name="Отображать")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ru:product_detail', args={self.slug})


class User(models.Model):
    pass