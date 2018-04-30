from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('payment', views.payment, name='payment'),
    path('my_room', views.my_room, name='my_room')
]

urlpatterns += [
    path('', views.ProductsListView.as_view(), name='products_list'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
]