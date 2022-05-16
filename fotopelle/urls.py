"""
Saraksts “urlpatterns” novirza vietrāžus (URL) uz skatiem.

https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
