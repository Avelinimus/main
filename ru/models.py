from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    pass


class Products(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок новости")
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, help_text='Нужно использовать для создания "хороших" URL-ов')
    image = models.ImageField(upload_to='products/img/%Y/%m/%d/', blank=True,
                              verbose_name="Картинка для новостей (300 x 300)")
    short_description = models.TextField(blank=True, verbose_name="Короткое описание в листе")
    description = RichTextUploadingField(blank=True, verbose_name="Детальное описание")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    available = models.BooleanField(default=True, verbose_name="Отображать")


class User(models.Model):
    pass