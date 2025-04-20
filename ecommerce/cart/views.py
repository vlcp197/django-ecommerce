import random
import string
from django.shortcuts import get_object_or_404, render
from core.models import Product

def cart(request):

    return render(request, 'cart/cart.html', {})


def generate_order_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def add_to_cart(request, slug):
    product = get_object_or_404(Product)
    ...

def remove_from_cart():
    ...

def update_cart():
    ...

def checkout_view():
    ...

def order_success():
    ...