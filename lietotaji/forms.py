from django.contrib.auth.forms import UserCreationForm
from .models import Lietotajs
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import TextInput
import re
from django.contrib.auth.password_validation import validate_password


# Priekš telefona ievades lauka:
class TelefonaIevade(TextInput):
    input_type = 'tel'


# Modificēta reģistrācijas veidlapa (form):
class RegistracijasVeidlapa(UserCreationForm):
    epasts = forms.EmailField(max_length=64, widget=forms.EmailInput())
    vards = forms.CharField(max_length=32, widget=forms.TextInput(),
                            error_messages={"required": "Vārdam ir jābūt norādītam!"})
    uzvards = forms.CharField(max_length=32, widget=forms.TextInput(),
                              error_messages={"required": "Uzvārdam ir jābūt norādītam!"})
    telefona_numurs = forms.CharField(max_length=15, widget=TelefonaIevade(
        attrs={"pattern": "(\+371)?\s?[0-9]{2}[-\s]?[0-9]{3}[-\s]?[0-9]{3}", "value": "+371 ",
               "autocomplete": "id_telefona_numurs"}))

    class Meta:
        model = Lietotajs
        fields = ("epasts", "vards", "uzvards", "telefona_numurs", "password1", "password2")

    # Pievieno katram ievades laukam klasi "form-control":
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for lauks in self.fields:
            widget_attrs = {"class": "form-control"}
            self.fields[str(lauks)].widget.attrs.update(widget_attrs)

    # Pārveido (iztīra) e-pasta adresi (pārtaisa lielos burtus uz mazajiem):
    def clean_epasts(self):
        epasts = self.cleaned_data["epasts"]
        return epasts.lower()

    # Validājija reģistrēšanās veidlapai:
    def clean(self):
        dati = super(RegistracijasVeidlapa, self).clean()

        parole = dati.get("password1")

        # Pārbauda vai parole ir pietiekami gara:
        garums = 8
        if len(parole) < garums:
            zina = "Parolei ir jābūt vismaz " + str(garums) + " rakstu zīmēm garai!"
            self.add_error("password1", zina)

        # Pārbauda vai parole satur ciparu:
        if sum(simbols.isdigit() for simbols in parole) < 1:
            zina = "Parolei ir jāsatur vismaz 1 cipars!"
            self.add_error("password1", zina)

        # Pārbauda vai parole satur kādu mazo burtu:
        if not any(simbols.islower() for simbols in parole):
            zina = "Parolei ir jāsatur vismaz 1 mazais burts!"
            self.add_error("password1", zina)

        # Pārbauda vai parole satur kādu lielo burtu:
        if not any(simbols.isupper() for simbols in parole):
            zina = "Parolei ir jāsatur vismaz 1 lielais burts!"
            self.add_error("password1", zina)

        # Pārbauda vai abas paroles sakrīt:
        apstiprinat_paroli = dati.get("password2")
        if parole and apstiprinat_paroli:
            if parole != apstiprinat_paroli:
                zina = "Abām parolēm ir jāsakrīt!"
                self.add_error("password2", zina)

        # Pārbauda vai parole satur lietotāja vārdu, uzvārdu vai epastu:
        modificeta_parole = parole.lower()

        vards = dati.get("vards")
        if vards:
            if vards in modificeta_parole:
                zina = "Parole nedrīkst būt līdzīga vārdam!"
                self.add_error("password1", zina)
        uzvards = dati.get("uzvards")
        if uzvards:
            if uzvards in modificeta_parole:
                zina = "Parole nedrīkst būt līdzīga uzvārdam!"
                self.add_error("password1", zina)
        epasts = dati.get('epasts')
        modificets_epasts = re.split("_ |\.", epasts.lower().split("@")[0])
        if any(virkne in modificeta_parole for virkne in modificets_epasts):
            zina = "Parole nedrīkst būt līdzīga epastam!"
            self.add_error("password1", zina)

        # Pārbauda vai epasta adrese ir unikālā (ka tāda datubāzē jau neeksistē):
        if Lietotajs.objects.filter(epasts=epasts).exists():
            zina = "Lietotājs ar tādu epastu jau eksistē!"
            self.add_error("epasts", zina)

        return dati


# Modificēta profila rediģēšanas veidlapa (form):
class ProfilaRedigesanasVeidlapa(UserChangeForm):
    epasts = forms.EmailField(max_length=64, widget=forms.EmailInput(attrs={'class': "form-control"}))
    vards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    uzvards = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    telefona_numurs = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': "form-control", "pattern": "(\+371)?\s?[0-9]{2}[-\s]?[0-9]{3}[-\s]?[0-9]{3}",
               "value": "+371 "}))
    profila_bilde = forms.ImageField()

    class Meta:
        model = Lietotajs
        fields = ("epasts", "vards", "uzvards", "telefona_numurs", "profila_bilde")
