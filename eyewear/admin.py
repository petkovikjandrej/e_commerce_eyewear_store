# admin.py

from django.contrib import admin
from .models import Product, Cart, CartItem, Color, Order, OrderItem

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Color)
admin.site.register(Order)
admin.site.register(OrderItem)