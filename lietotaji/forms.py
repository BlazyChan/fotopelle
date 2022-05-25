from django.contrib.auth.forms import UserCreationForm
from .models import Lietotajs
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import TextInput
from django.contrib.auth.password_validation import validate_password


# Priekš telefona ievades lauka:
class TelefonaIevade(TextInput):
    input_type = 'tel'



# Modificēta reģistrācijas veidlapa (form):
class RegistracijasVeidlapa(UserCreationForm):
    epasts = forms.EmailField(max_length=64, widget=forms.EmailInput())
    vards = forms.CharField(max_length=32, widget=forms.TextInput())
    uzvards = forms.CharField(max_length=32, widget=forms.TextInput())
    telefona_numurs = forms.CharField(max_length=15, widget=TelefonaIevade(attrs={"pattern": "(\+371)?\s?[0-9]{2}[-\s]?[0-9]{3}[-\s]?[0-9]{3}", "value": "+371 "}))

    class Meta:
        model = Lietotajs
        fields = ("epasts", "vards", "uzvards", "telefona_numurs", "password1", "password2")

    # Pievieno katram ievades laukam klasi "form-control":
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for lauks in self.fields:
            widget_attrs = {"class": "form-control"}
            self.fields[str(lauks)].widget.attrs.update(widget_attrs)


# Modificēta profila rediģēšanas veidlapa (form):
class ProfilaRedigesanasVeidlapa(UserChangeForm):
    epasts = forms.EmailField(max_length=64, widget=forms.EmailInput(attrs={'class': "form-control"}))
    vards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    uzvards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    telefona_numurs = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': "form-control", "pattern": "(\+371)?\s?[0-9]{2}[-\s]?[0-9]{3}[-\s]?[0-9]{3}", "value": "+371 "}))
    profila_bilde = forms.ImageField()

    class Meta:
        model = Lietotajs
        fields = ("epasts", "vards", "uzvards", "telefona_numurs", "profila_bilde")
