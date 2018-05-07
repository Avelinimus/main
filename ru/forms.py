from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Order


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], initial='1', label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code',
                  'city']

