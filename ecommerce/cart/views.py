import random
import string
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from core.models import Product


def cart(request):

    return render(request, 'cart/cart.html', {})


def generate_order_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})

    if slug in cart:
        cart[slug]["quantity"] += 1
    else:
        cart[slug] = {
            'quantity': 1,
            'preco_unitario': float(product.price)
        }
    
    request.session['cart'] = cart
    messages.success(request, f"{product.name} adicionado ao carrinho")
    return redirect('core.home')

def remove_from_cart(request, slug):
    cart = request.session.get('cart', {})

    if slug in cart:
        del cart[slug]
        request.session["cart"] = cart 
        messages.success(request, "Item removido do carrinho")

    return redirect('cart')


def update_cart(request):
    if request.method == 'POST':
        ...

def checkout_view():
    ...

def order_success():
    ...