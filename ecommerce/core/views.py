from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html', {})

def product_detail(request, product_id):
    return render(request, 'core/product_detail.html', {"product_id": product_id})

def cart(request):
    return render(request, 'core/cart.html')