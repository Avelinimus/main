from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('payment', views.payment, name='payment')
]

urlpatterns += [
    path('', views.ProductsListView.as_view(), name='products_list'),

]