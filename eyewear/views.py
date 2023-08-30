from _decimal import Decimal

import stripe
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from eyewear.models import Product, Color, Cart, CartItem, Order, OrderItem
from .forms import ProductForm


# Create your views here.

def home(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})


def product_detail(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        return render(request, 'product_detail.html', {'product': product})


@login_required
def add_product(request):
    if not request.user.is_staff:
        return redirect('some_page_forbidden')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def update_product(request, pk):  # make sure to include 'pk' here
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'add_product.html', {'form': form, 'update_mode': True, 'product': product})


def delete_product(request, pk):
    if request.user.is_staff:  # check if user is admin
        product = Product.objects.get(pk=pk)
        product.delete()
        return redirect('/')
    else:
        return HttpResponse('Unauthorized', status=401)


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'view_cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        selected_color_id = request.POST.get('color_choice')

        if not selected_color_id:
            # The color wasn't selected; return a flag that will trigger the toast.
            return JsonResponse({'status': 'fail', 'message': 'Please select a color.'})

        selected_color = Color.objects.get(id=selected_color_id)
        product = Product.objects.get(id=product_id)
        input_quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided

        user_cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=product,
            defaults={'quantity': 0}
        )

        # Now use input_quantity instead of always incrementing by 1
        cart_item.quantity += input_quantity
        cart_item.color = selected_color
        cart_item.save()

        # Update the total_price of the cart
        user_cart.total_price = Decimal(user_cart.total_price) + (
                    product.price * input_quantity)  # Adjust based on the input quantity
        user_cart.save()

        return JsonResponse({'status': 'success', 'message': 'Item added to cart.'})

    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request.'})


@login_required
def remove_from_cart(request, product_id):
    user_cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=user_cart, product_id=product_id)

    # Reduce the total_price of the cart
    user_cart.total_price -= cart_item.product.price * cart_item.quantity
    user_cart.save()

    # Delete the cart item
    cart_item.delete()

    return redirect('view_cart')


@login_required
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    user_cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        stripe_token = request.POST.get('stripeToken')

        try:
            charge = stripe.Charge.create(
                amount=int(user_cart.total_price * 100),
                currency='usd',
                description=f"Order from {request.user}",
                source=stripe_token,
            )
            new_order = Order.objects.create(
                user=request.user,
                total_price=user_cart.total_price,
                is_complete=True,
            )
            for item in user_cart.items.all():
                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    color=item.color,
                    quantity=item.quantity
                )
            user_cart.items.all().delete()
            user_cart.total_price = 0
            user_cart.save()
            return redirect('order_complete')
        except stripe.error.StripeError as e:
            return render(request, 'checkout.html', {'error': str(e), 'cart': user_cart, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})

    return render(request, 'checkout.html', {'cart': user_cart, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})


@login_required
def order_complete(request):
    return render(request, 'order_complete.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Or another page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Or another page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
