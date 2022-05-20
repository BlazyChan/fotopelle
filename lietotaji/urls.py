from django.urls import path
from . import views

urlpatterns = [
    path('pieslegties/', views.pieslegties, name="pieslēgties"),
    path('registreties/', views.registreties, name="reģistrēties"),
    path('izrakstities/', views.izrakstities, name="izrakstīties"),
]
