from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages 
from . import models
from . import forms

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = models.Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "Este produto não existe... Por favor, pesquise novamente")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        # Get current User
        current_user =  models.Profile.objects.get(user__id=request.user.id)
        # Get current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get Original User Form
        form = forms.UserInfoForm(request.POST or None, instance = current_user)
        # Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            #save original form
            form.save()
            # save shipping form
            shipping_form.save()
            messages.success(request, "Suas informações foram atualizadas")

            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "Você precisa estar logado para acessar esta página")
        return redirect('home')


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

            current_user = models.Profile.objects.get(user__id=request.user.id)

            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("Você logou com sucesso"))
            return redirect('home')
        else:
            messages.success(request, ("Ocorreu um erro, tente novamente"))
            return redirect('home')
    else:
        return render(request, 'login.html',{})

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
            messages.success(request, ("Usuário criado, por favor preencha suas informações de usuário abaixo"))
            return redirect("update_info")
        else:
            messages.success(request, ("Houve um problema com o registro. Por favor, tente novamente"))
            return redirect("register")
    return render(request, 'register.html', {'form':form })
