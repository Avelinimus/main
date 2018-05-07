from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('payment/', views.payment, name='payment'),
    path('my_room/', views.my_room, name='my_room')
]

urlpatterns += [
    path('', views.CategoryListView.as_view(), name='category_list'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^product/(?P<slug>[\w-]+)/$', views.product_detail, name='product_detail')
]

urlpatterns += [
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^cart/$', views.cart_detail, name='cart_detail'),
    url(r'^create_order/$', views.order_create, name='order_create')

]