from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import HiddenInput

from .models import Order, Profile, Comments, Support


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], initial='1',
                                  label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                  'city']
        widgets = {
            'user': HiddenInput,
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'city', 'postal_code', 'number_phone', 'birth_date')


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['title', 'comments_text']
        widgets = {
            'author': HiddenInput,
        }



class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['title', 'first_name', 'last_name', 'email', 'number_phone', 'description']
