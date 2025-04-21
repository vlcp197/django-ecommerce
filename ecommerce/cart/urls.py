from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('adicionar/<slug:slug>/', views.add_to_cart,name="add_to_cart"),
    path('remover/<slug:slug>/', views.remove_from_cart,name="remove_from_cart"),
    path('atualizar/<slug:slug>/', views.update_cart,name="update_cart"),
    path('checkout/', views.checkout_view,name="checkout"),
    path('pedido-sucesso/<str:codigo>/', views.order_success, name="order_success"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)