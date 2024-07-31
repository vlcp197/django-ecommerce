from django.urls import path
from . import views
from ecommerce import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
