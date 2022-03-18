from django.contrib import admin
from django.urls import path
from core.views import home, about, contact, blog, events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('blog/', blog, name="blog"),
    path('events/', events, name="events"),
    
    
]
