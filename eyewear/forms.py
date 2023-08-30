from django import forms
from django.forms import ModelMultipleChoiceField

from .models import Product, Color


class ProductForm(forms.ModelForm):
    colors_available = ModelMultipleChoiceField(queryset=Color.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo', 'quantity_available', 'brand', 'product_type',
                  'colors_available']
