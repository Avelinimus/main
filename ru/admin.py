from django.contrib import admin
from ru.models import Products, Category


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available']
    list_editable = ['available']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'available', 'created']
    list_filter = ['category', 'available', 'created']
    list_editable = ['available', 'category']
    search_fields = ['name', 'category']
    prepopulated_fields = {'slug': ('name',)}

