from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Color(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='color_images/')

    def __str__(self):
        return self.name


class Product(models.Model):
    EYEGLASSES = 'EG'
    SUNGLASSES = 'SG'
    LENSES = 'LS'
    OTHER = 'OT'

    PRODUCT_CHOICES = [
        (EYEGLASSES, 'Eyeglasses'),
        (SUNGLASSES, 'Sunglasses'),
        (LENSES, 'Lenses'),
        (OTHER, 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='product_photos/')
    colors_available = models.ManyToManyField(Color)
    quantity_available = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=100)
    product_type = models.CharField(
        max_length=2,
        choices=PRODUCT_CHOICES,
        default=EYEGLASSES,
    )


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_complete = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
