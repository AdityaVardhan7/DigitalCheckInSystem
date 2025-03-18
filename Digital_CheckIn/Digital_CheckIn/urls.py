from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import set_language


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),  # Include checkin_system URLs
    path('set_language/', set_language, name='set_language'),  # Language switch URL

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

