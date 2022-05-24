from django import forms
from django.forms import ModelForm
from .models import Pasutijums, PakalpojumaVeids, BilzuGalerija, Bilde


# Priekš skaistākas/vieglākas datuma/laika ievadīšanas:
class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


# Pasūtījuma modeļa Veidlapa:
class PasutijumaVeidlapa(ModelForm):
    pasutijuma_datums = forms.DateTimeField(widget=DateTimeInput())

    # Jāaprēķina:
    kopeja_cena = forms.FloatField(widget=forms.NumberInput())

    apraksts = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Pasutijums
        fields = ("pasutijuma_datums", "kopeja_cena", "pakalpojuma_veids", "apraksts",)

    # Pievieno katram ievades laukam klasi "form-control":
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for lauks in self.fields:
            widget_attrs = {"class": "form-control"}
            self.fields[str(lauks)].widget.attrs.update(widget_attrs)
