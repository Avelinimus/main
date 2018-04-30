from django.contrib import admin
from ru.models import Products, Category


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available', 'created']
    list_filter = ['name', 'available', 'created']
    list_editable = ['available']
    search_fields = ['name', 'category']
    prepopulated_fields = {'slug': ('name',)}
