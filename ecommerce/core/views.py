import random
from django.shortcuts import get_object_or_404, render
from .models import Product
import string

def home(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})

def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)

    quantity = request.session.get('cart')[slug]["quantity"]

    return render(request, 'core/product_detail.html', {"product": product, "quantity": quantity })

