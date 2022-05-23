from django.contrib.auth.forms import UserCreationForm
from .models import Lietotajs
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.password_validation import validate_password


# Modificēta reģistrācijas veidlapa (form):
class RegistracijasVeidlapa(UserCreationForm):
    epasts = forms.EmailField(max_length=64, widget=forms.EmailInput(attrs={'class': "form-control"}))
    vards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    uzvards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    telefona_numurs = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = Lietotajs
        fields = ("epasts", "vards", "uzvards", "telefona_numurs")


# Modificēta profila rediģēšanas veidlapa (form):
class ProfilaRedigesanasVeidlapa(UserChangeForm):
    epasts = forms.EmailField(max_length=64, widget=forms.EmailInput(attrs={'class': "form-control"}))
    vards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    uzvards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    telefona_numurs = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': "form-control"}))
    profila_bilde = forms.ImageField()

    class Meta:
        model = Lietotajs
        fields = ("epasts", "vards", "uzvards", "telefona_numurs", "profila_bilde")
