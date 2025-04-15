from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})

def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)
    return render(request, 'core/product_detail.html', {"product": product})

def cart(request):
    return render(request, 'core/cart.html')