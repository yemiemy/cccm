from django.contrib import admin
from django.urls import path, include
from core.views import home, about, contact, blog, events

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

admin.site.site_header = "CCCM Admin"
admin.site.site_title = "CCCM Admin Portal"
admin.site.index_title = "Welcome to CCCM Portal"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
