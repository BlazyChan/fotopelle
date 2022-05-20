from django.contrib.auth.forms import UserCreationForm
from .models import Lietotajs


# Modificēta reģistrācijas veidlapa (form):
class RegistracijasVeidlapa(UserCreationForm):
    class Meta:
        model = Lietotajs
        fields = ("epasts", "vards", "uzvards", "telefona_numurs", "password1", "password2")
