from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from ru.models import Products, Category, Profile
from ru.models import Order, OrderItem
from ru.models import Comments, Support
from ru.models import Contact, Payment
from django.http import HttpResponse
import csv
import datetime


# Register your models here.


def export_to_CSV(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
        filename=Orders-{}.csv'.format(datetime.datetime.now().strftime("%d/%m/%Y"))
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Первая строка- оглавления
    writer.writerow([field.verbose_name for field in fields])
    # Заполняем информацией
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


def order_detail(obj):
    return format_html('<a href="{}">Посмотреть</a>'.format(
        reverse('ru:admin_order_detail', args=[obj.id])
    ))


"""
def order_PDF(obj):
    return format_html('<a href="{}">PDF</a>'.format(
        reverse('ru:admin_order_PDF', args=[obj.id])
    ))
"""

export_to_CSV.short_description = 'Export CSV'
# order_PDF.short_description = 'В PDF'


class ProductsInline(admin.StackedInline):
    model = Comments
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available']
    list_editable = ['available']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'available', 'created', 'discount']
    list_filter = ['category', 'available', 'created']
    list_editable = ['available', 'category']
    search_fields = ['name', 'category']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductsInline]


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'number_phone', 'created', 'verified']
    list_filter = ['verified']
    list_editable = ['verified']
    search_fields = ['title', 'email', 'number_phone']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['address', 'postal_code', 'city', 'number_phone']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'sent', 'take_client', 'created', 'updated', order_detail]
    list_editable = ['paid', 'sent', 'take_client']
    list_filter = ['paid', 'created', 'updated', 'paid', 'sent']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'address', 'city']
    inlines = [OrderItemInline]
    actions = [export_to_CSV]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

    list_display = ['title', 'description']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

    list_display = ['title', 'description']


