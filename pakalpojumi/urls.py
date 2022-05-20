from django.urls import path
from . import views

urlpatterns = [
    path('', views.pasutit, name="pasūtīt"),
]
