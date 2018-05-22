from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('payment/', views.payment, name='payment'),
    path('my-room/', views.my_room, name='my_room'),
    path('support/', views.support, name='support'),
]

urlpatterns += [
    path('', views.category_list_view, name='category_list'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category_detail_view, name='category_detail'),
    url(r'^product/(?P<slug>[\w-]+)/$', views.product_detail_view, name='product_detail'),
    url(r'^shares', views.shares_list_view, name='shares_list')
]

urlpatterns += [
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^add-comment/(?P<product_id>\d+)/$', views.comment_add, name='comment_add'),
    url(r'^cart_detail/$', views.cart_detail, name='cart_detail'),
    url(r'^create_order/$', views.order_create, name='order_create'),
    url(r'^admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
    # url(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.admin_order_PDF, name='admin_order_PDF')
]
