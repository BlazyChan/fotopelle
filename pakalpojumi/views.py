from django.core.files.images import get_image_dimensions
from django.shortcuts import render, redirect
from .forms import PasutijumaVeidlapa
from django.contrib import messages
from .models import PakalpojumaVeids, Pasutijums, BilzuGalerija, Bilde
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from lietotaji.models import Fotografs
import base64
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils.crypto import get_random_string


# Lapas "Pasūtīt" mainīgie:
gala_bildes = None
gala_galerija = None


# Sākumlapa (pirmā lapa, ko redz atverot mājaslapu):
def sakumlapa(request):
    # Tiek iegūti pakalpojuma nosaukumi, apraksti un cenas:
    pakalpojumu_apraksti = PakalpojumaVeids.objects.filter()
    # Pārveido modeli par JSON simbolu virkni:
    pakalpojumu_apraksti = serializers.serialize("json", pakalpojumu_apraksti, cls=DjangoJSONEncoder)

    # Tiek iegūta informācija par fotogrāfiem (paigaidām vienu):
    fotografu_apraksti = Fotografs.objects.filter()
    # Pārveido modeli par JSON simbolu virkni:
    # fotografu_apraksti = serializers.serialize("json", fotografu_apraksti, cls=DjangoJSONEncoder)

    return render(request, 'sakumlapa.html', {"pakalpojumu_apraksti": pakalpojumu_apraksti, "fotografu_apraksti": fotografu_apraksti})


# Lapa, kur lietotājs var veikt pasūtījumus, jeb pasūtīt pakalpojumus:
def pasutit(request):
    if request.user.is_anonymous is False:
        global gala_bildes
        global gala_galerija

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            gala_bildes = request.POST.getlist('django_bildes[]')
            form = PasutijumaVeidlapa()

        elif request.method == "POST":
            form = PasutijumaVeidlapa(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.lietotajs = request.user
                instance.pakalpojuma_veids = PakalpojumaVeids.objects.get(nosaukums=instance.pakalpojuma_veids)
                instance.save()

                # Izveido jaunu bilžu galeriju:
                gala_galerija = BilzuGalerija.objects.create(
                    nosaukums=str(instance.pakalpojuma_veids) + " - " + instance.lietotajs.vards + " " + instance.lietotajs.uzvards + " (" + str(instance.pasutijuma_datums) + ")", pasutijums=instance)

                # Veiksmīga pasūtījuma izveidošanas gadījumā - lietotāju aizved uz norādīto lapu un izvada ziņu:
                messages.success(request, "Pasūtījums tika veiksmīgi izveidots!")
                return redirect('/pasutit/')
        else:
            form = PasutijumaVeidlapa()

        vaicajums = PakalpojumaVeids.objects.filter()
        # Pārveido modeli par JSON simbolu virkni:
        vaicajums = serializers.serialize("json", vaicajums, cls=DjangoJSONEncoder)

        # Ja abi mainīgie eksistē, tad izveido bildes objektus:
        if gala_bildes and gala_galerija:
            bilzu_galerija = gala_galerija
            bildes = gala_bildes
            for bilde in bildes:
                base64_fails = bilde.split("base64,")[1]
                satura_veids = bilde.split(";")[0].split("data:")[1].split("+")[0]
                bildes_nosaukums = get_random_string(7) + "." + satura_veids.split("/")[1]

                f = io.BytesIO(base64.b64decode(base64_fails))
                bilde = InMemoryUploadedFile(f, field_name='picture', name=bildes_nosaukums, content_type=satura_veids,
                                             size=sys.getsizeof(f), charset=None)
                # Izveido bildes objektu:
                Bilde.objects.create(
                    atrasanas_vieta=str('lietotajs_{0}/{1}/'.format(str(request.user.epasts.replace("@", "_")),
                                                                    str(bilzu_galerija.id) + "_" + str(
                                                                        bilzu_galerija.nosaukums))),
                    fails=bilde,
                    lietotajs=request.user,
                    bilzu_galerija=bilzu_galerija
                )
            gala_galerija = None
            gala_bildes = None
        return render(request, 'pasutit.html', {"form": form, "pakalpojumu_apraksti": vaicajums})
    else:
        return redirect("/")


# Lapa, kurā parasts lietotājs var apskatīt savus vai fotogrāfs var apskatīt visus pasūtījumus:
def pasutijumi(request):
    if request.user.is_anonymous is False:
        # Ja lietotājs ir fotogrāfs, tad izvada visus pasūtījumus:
        if Fotografs.objects.filter(lietotajs=request.user.epasts).exists() or request.user.is_superuser:
            virsraksts = "Visi pasūtījumi"
            vaicajums = Pasutijums.objects.all()
            ir_fotografs = True
        # Ja lietotājs nav fotogrāfs, tad izvada visus šī paša lietotāja pasūtījumus:
        else:
            virsraksts = "Mani pasūtījumi"
            vaicajums = Pasutijums.objects.filter(lietotajs=request.user)
            ir_fotografs = False
        # Pasūtījumu skaits:
        skaits = vaicajums.count()
        return render(request, 'pasutijumi.html', {"pasutijumi": vaicajums, "virsraksts": virsraksts, "skaits": skaits, "diapazona": range(int(skaits)), "ir_fotografs": ir_fotografs})
    else:
        return redirect("/")


# Bilžu galerijas lapa (balstoties uz pasūtījumu):
def bilzu_galerijas_saite(request, id):
    id = str(id)
    if Pasutijums.objects.filter(id=id):
        pasutijums = Pasutijums.objects.get(id=id)
        if request.user.is_anonymous:
            return redirect('/pasutijumi/')
        else:
            # if request.user.epasts == pasutijums.fotografs or request.user.is_superuser:
            if Fotografs.objects.filter(lietotajs=request.user.epasts) or request.user.is_superuser:
                ir_fotografs = True
                # Ja fotogrāfs vai super lietotājs mēģina saglabāt jaunas bildes:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
                    bilzu_galerija = BilzuGalerija.objects.get(pasutijums=pasutijums)
                    bildes = request.POST.getlist('django_bildes[]')
                    if bildes and bilzu_galerija:
                        for bilde in bildes:
                            base64_fails = bilde.split("base64,")[1]
                            satura_veids = bilde.split(";")[0].split("data:")[1].split("+")[0]
                            bildes_nosaukums = get_random_string(7) + "." + satura_veids.split("/")[1]

                            f = io.BytesIO(base64.b64decode(base64_fails))
                            bilde = InMemoryUploadedFile(f, field_name='picture', name=bildes_nosaukums,
                                                         content_type=satura_veids,
                                                         size=sys.getsizeof(f), charset=None)
                            # Izveido bildes objektu:
                            Bilde.objects.create(
                                atrasanas_vieta=str('lietotajs_{0}/{1}/'.format(str(pasutijums.lietotajs.epasts.replace("@", "_")),
                                                                                str(bilzu_galerija.id) + "_" + str(
                                                                                    bilzu_galerija.nosaukums))),
                                fails=bilde,
                                lietotajs=request.user,
                                bilzu_galerija=bilzu_galerija
                            )
            else:
                ir_fotografs = False

            # Ja bilžu galerijā ir bildes:
            if BilzuGalerija.objects.filter(pasutijums=pasutijums.id):
                galerija = BilzuGalerija.objects.get(pasutijums=pasutijums.id)
                bildes = Bilde.objects.filter(bilzu_galerija=galerija.id)

                # Bilžu kopējais skaits galerijā:
                skaits = bildes.count()

                # Pārbauda vai bilžu galerijas bildes pieder pašreizējam lietotājam:
                if bildes.filter(lietotajs=request.user):
                    pasa_bildes = True
                else:
                    pasa_bildes = False

                return render(request, 'galerija.html',
                              {"galerija": galerija, "bildes": bildes, "skaits": skaits, "ir_fotografs": ir_fotografs, "id": id, "pasa_bildes": pasa_bildes})
            else:
                return redirect('/pasutijumi/')
    else:
        return redirect('/pasutijumi/')


# Bilžu izdzēšana, balstoties uz pasūtījumu un lietotāju:
def izdzest_bildes(request, id):
    bilzu_galerija = BilzuGalerija.objects.get(pasutijums=id)
    bildes = Bilde.objects.filter(bilzu_galerija_id=bilzu_galerija.id, lietotajs=request.user)
    bildes.delete()
    return redirect("/galerijas/" + id + "/")
