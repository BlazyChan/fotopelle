from django.shortcuts import render, redirect
from .forms import PasutijumaVeidlapa
from django.contrib import messages
from .models import PakalpojumaVeids, Pasutijums
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


# Sākumlapa (pirmā lapa, ko redz atverot mājaslapu):
def sakumlapa(request):
    return render(request, 'sakumlapa.html', {})


# Lapa, kur lietotājs var veikt pasūtījumus, jeb pasūtīt pakalpojumus:
def pasutit(request):
    if request.method == "POST":
        form = PasutijumaVeidlapa(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.lietotajs = request.user
            instance.pakalpojuma_veids = PakalpojumaVeids.objects.get(nosaukums=instance.pakalpojuma_veids)
            instance.save()

            # Veiksmīga pasūtījuma izveidošanas gadījumā - lietotāju aizved uz norādīto lapu un izvada ziņu:
            messages.success(request, "Pasūtījums tika veiksmīgi izveidots!")
            return redirect('/pasutit/')
    else:
        form = PasutijumaVeidlapa()

    vaicajums = PakalpojumaVeids.objects.filter()

    # Pārveido modeli par JSON simbolu virkni:
    vaicajums = serializers.serialize("json", vaicajums, cls=DjangoJSONEncoder)
    return render(request, 'pasutit.html', {"form": form, "pakalpojumu_apraksti": vaicajums})


# Lapa, kurā parasts lietotājs var apskatīt savus vai fotogrāfs var apskatīt visus pasūtījumus:
def pasutijumi(request):
    vaicajums = Pasutijums.objects.all()
    return render(request, 'pasutijumi.html', {"pasutijumi": vaicajums})
