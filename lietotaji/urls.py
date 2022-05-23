from django.urls import path
from . import views
from .views import RedigetProfilu

urlpatterns = [
    path('pieslegties/', views.pieslegties, name="pieslēgties"),
    path('registreties/', views.registreties, name="reģistrēties"),
    path('izrakstities/', views.izrakstities, name="izrakstīties"),
    path('rediget_profilu/', RedigetProfilu.as_view(), name="rediģēt profilu"),
]
