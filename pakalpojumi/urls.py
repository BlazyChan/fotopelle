from django.urls import path
from . import views

urlpatterns = [
    path('', views.sakumlapa, name="sākumlapa"),
    path('pasutit/', views.pasutit, name="pasūtīt"),
    path('pasutijumi/', views.pasutijumi, name="pasūtījumi"),
    path('galerijas/<str:id>/', views.bilzu_galerijas_saite, name="galerija"),
    path('izdzest_bildes/<str:id>/', views.izdzest_bildes, name="izdzēst bildes"),
]
