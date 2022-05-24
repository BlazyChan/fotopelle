from django.urls import path
from . import views

urlpatterns = [
    path('', views.sakumlapa, name="sākumlapa"),
    path('pasutit/', views.pasutit, name="pasūtīt"),
    path('pasutijumi/', views.pasutijumi, name="pasūtījumi"),
]
