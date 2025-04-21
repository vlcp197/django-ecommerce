import random
import string
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from core.models import Product
from cart.models import Order


def cart(request):

    cart = request.session.get('cart', {})

    items = []
    total = 0

    for product_slug, item in cart.items():
        product = get_object_or_404(Product, slug=product_slug)
        subtotal = product.price  * item['quantity']
        items.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })
        total += subtotal
        

    return render(request, 'cart/cart.html', {
        'items': items,
        "total": total
    })


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
    return redirect('home')

def remove_from_cart(request, slug):
    cart = request.session.get('cart', {})

    if slug in cart:
        del cart[slug]
        request.session["cart"] = cart 
        messages.success(request, "Item removido do carrinho")

    return redirect('cart')


def update_cart(request, slug):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, slug=slug)

        cart = request.session.get('cart', {})

        if quantity > 0:
            cart[slug]['quantity'] = quantity
            request.session['cart'] = cart
        else:
            return remove_from_cart(request, slug)

def checkout_view(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    total = sum(
        item['quantity'] * item['price'] for item in cart.values()
    )
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        order = Order.objects.create(
            code=generate_order_code(),
            total=total,
            client_name=name,
            email=email,
            address=address
        )

        del request.session['cart']


        return redirect('order_success', code=order.code)

    return render(request, 'cart/checkout.html', {total: total})


def order_success(request, code):
    order = get_object_or_404(Order, code=code)
    return render(request, 'cart/order_success.html', {'order': order})
    