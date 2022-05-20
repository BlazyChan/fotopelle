"""
Saraksts “urlpatterns” novirza vietrāžus (URLs) uz skatiem.

https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django administrātora lapas URL:
    path('admin/', admin.site.urls),

    # Lietnotnes "lietotaji" URLs:
    path('', include('django.contrib.auth.urls')),
    path('', include('lietotaji.urls')),

    # Lietnotnes "pakalpojumi" URLs:
    path('', include('pakalpojumi.urls')),
]
