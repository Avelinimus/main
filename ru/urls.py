from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('payment', views.payment, name='payment'),
    path('my_room/()', views.my_room, name='my_room')
]

urlpatterns += [
    path('', views.CategoryListView.as_view(), name='category_list'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^product/(?P<id>\d+)/(?P<slug>[-\w]+)]/$', views.product_detail, name='product_detail')
]