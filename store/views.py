from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from . import models

def home(request):
    products = models.Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html',)

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("Você logou com sucesso"))
            return redirect('home')
        else:
            messages.success(request, ("Ocorreu um erro, tente novamente"))
            return redirect('home')
    return render(request, 'login.html',)

def logout_user(request):
    logout(request)
    messages.success(request, ("Você deslogou"))
    return redirect("home")
