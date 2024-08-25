from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages 
from . import models
from . import forms

def update_user(request):
    if request.user.is_authenticated:
        current_user =  User.objects.get(id=request.user.id)
        user_form = forms.UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Usuário foi atualizado")

            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "Você precisa estar logado para acessar esta página")
        return redirect('home')

def category_summary(request):
    categories = models.Category.objects.all()
    return render(request, "category_summary.html", {"categories":categories})

def category(request, foo):
    foo = foo.replace("-", " ")
    try:
        category = models.Category.objects.get(name=foo)
        products = models.Product.objects.filter(category=category)
        return render(request, "category.html", {"products": products, "category": category})
    except:
        messages.success(request, ("Essa categoria não existe")) 
        return redirect("home")


def product(request, pk):
    product = models.Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

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
    else:
        return render(request, 'login.html',)

def logout_user(request):
    logout(request)
    messages.success(request, ("Você deslogou"))
    return redirect("home")

def register_user(request):
    form = forms.SignUpForm()
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Bem vindo. Você se registrou com sucesso"))
            return redirect("home")
        else:
            messages.success(request, ("Houve um problema com o registro. Por favor, tente novamente"))
            return redirect("home")
    return render(request, 'register.html', {'form':form })
