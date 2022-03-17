from django.contrib import admin
from django.urls import path
from core.views import home, about, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact")
]
