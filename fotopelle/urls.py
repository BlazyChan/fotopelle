"""
Saraksts “urlpatterns” novirza vietrāžus (URLs) uz skatiem.

https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Django administrātora lapas URL:
    path('admin/', admin.site.urls),

    # Lietnotnes "lietotaji" URLs:
    path('', include('django.contrib.auth.urls')),
    path('', include('lietotaji.urls')),

    # Lietnotnes "pakalpojumi" URLs:
    path('', include('pakalpojumi.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Izveido/norāda saiti uz bildēm
