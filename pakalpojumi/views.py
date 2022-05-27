from django.shortcuts import render, redirect
from .forms import PasutijumaVeidlapa
from django.contrib import messages
from .models import PakalpojumaVeids, Pasutijums, BilzuGalerija, Bilde
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

            # Izveido jaunu bilžu galeriju:
            bilzu_galerija = BilzuGalerija.objects.create(
                nosaukums=str(
                    instance.pakalpojuma_veids) + " - " + request.user.vards + " " + request.user.uzvards + " (" + str(
                    instance.pasutijuma_datums) + ")",
                pasutijums=instance,
            )

            # Saglabā katru augšupielādēto bildi (no "bilžu izdrukas" pasūtījuma veida):
            if instance.pakalpojuma_veids.nosaukums == "Bilžu izdruka":
                bildes = request.FILES.getlist("bildes")
                for bilde in bildes:
                    Bilde.objects.create(
                        atrasanas_vieta=str('lietotajs_{0}/{1}/'.format(str(request.user.epasts.replace("@", "_")), str(bilzu_galerija.id) + "_" + str(bilzu_galerija.nosaukums))),
                        fails=bilde,
                        lietotajs=request.user,
                        bilzu_galerija=bilzu_galerija,
                    )

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


# Bilžu galerijas lapa (balstoties uz pasūtījumu):
def bilzu_galerijas_saite(request, id):
    pasutijums = Pasutijums.objects.get(id=id)
    galerija = BilzuGalerija.objects.get(pasutijums=pasutijums.id)
    bildes = Bilde.objects.filter(bilzu_galerija=galerija.id)
    return render(request, 'galerija.html', {"galerija": galerija, "bildes": bildes})
