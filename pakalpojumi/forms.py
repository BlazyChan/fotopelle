from django import forms
from django.forms import ModelForm
from .models import Pasutijums, PakalpojumaVeids, BilzuGalerija, Bilde
from datetime import datetime


# Pasūtījuma modeļa Veidlapa:
class PasutijumaVeidlapa(ModelForm):
    # Datumam jābūt šodienai vai vēlāk:
    pasutijuma_datums = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "min": datetime.now().date()}))

    pasutijuma_laiks = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time", "value": "00:00", "step": "300"}))

    # Jāaprēķina:
    kopeja_cena = forms.FloatField(widget=forms.NumberInput())

    apraksts = forms.CharField(widget=forms.Textarea(), required=False)


    class Meta:
        model = Pasutijums
        fields = ("pasutijuma_datums", "pasutijuma_laiks", "pakalpojuma_veids", "kopeja_cena", "apraksts",)

    # Pievieno katram ievades laukam klasi "form-control":
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for lauks in self.fields:
            widget_attrs = {"class": "form-control"}
            self.fields[str(lauks)].widget.attrs.update(widget_attrs)

        # Priekš pakalpojuma apraksta un galerijas (izsauc funkciju, kad pārmaina izvēlnes vērtību):
        self.fields["pakalpojuma_veids"].widget.attrs.update({"onchange": "PakalpojumaApraksts()"})
