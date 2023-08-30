# admin.py

from django.contrib import admin
from .models import Product, Cart, CartItem, Color

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Color)
