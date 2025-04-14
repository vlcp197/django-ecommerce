from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('produto/<int:product_id>/', views.product_detail, name="product-detail"),
    path('carrinho/', views.cart, name="cart"),
]