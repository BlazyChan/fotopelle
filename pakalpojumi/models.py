import os
import shutil
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from fotopelle.settings import MEDIA_ROOT
from lietotaji.models import Lietotajs, Fotografs, lietotaja_profila_bildes_cels
from datetime import date, timedelta
from django.utils import timezone


# Lietotāja pasūtījuma galerijas bildes ceļš:
def bilzu_galerijas_cels(self, filename):
    return '{0}/{1}'.format(self.atrasanas_vieta, filename)


# Pakalpojuma veida modelis:
class PakalpojumaVeids(models.Model):
    nosaukums = models.CharField(primary_key=True, max_length=128)
    apraksts = models.TextField()
    cena = models.FloatField()

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return self.nosaukums

    # Lai administratoru lapā modeļa nosaukums parādās akurāti:
    class Meta:
        verbose_name = "Pakalpojuma veids"
        verbose_name_plural = "Pakalpojuma veidi"


# Pasūtījuma modelis:
class Pasutijums(models.Model):
    id = models.AutoField(primary_key=True)

    # Vai pakalpojums ir aktīvs vai pabeigts (statuss)?
    aktivs = models.BooleanField(default=True, verbose_name="aktīvs")

    # Automātiski izveidots datums:
    pasutijuma_veiktais_datums = models.DateTimeField(auto_now_add=True, verbose_name="pasūtījuma veiktais datums")

    pasutijuma_datums = models.DateField(verbose_name="pasūtījuma datums")
    pasutijuma_laiks = models.TimeField(verbose_name="pasūtījuma laiks")

    apraksts = models.TextField(null=True)
    # Jāaprēķina:
    kopeja_cena = models.FloatField(null=True, verbose_name="kopējā cena")

    # Ārējās atslēgas:
    lietotajs = models.ForeignKey(Lietotajs, to_field="epasts", on_delete=models.CASCADE, verbose_name="lietotājs")
    pakalpojuma_veids = models.ForeignKey(PakalpojumaVeids, to_field="nosaukums", on_delete=models.SET_NULL, null=True)
    fotografs = models.ForeignKey(Fotografs, to_field="lietotajs", on_delete=models.SET_NULL, null=True,
                                  verbose_name="fotogrāfs")

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return str(self.id)

    # Lai administratoru lapā modeļa nosaukums parādās akurāti:
    class Meta:
        verbose_name = "Pasūtījums"
        verbose_name_plural = "Pasūtījumi"


# Bilžu galerija:
class BilzuGalerija(models.Model):
    id = models.AutoField(primary_key=True)
    nosaukums = models.CharField(max_length=128)
    izveidosanas_datums = models.DateTimeField(auto_now_add=True, verbose_name="izveidošanas datums")

    # Ārējā atslēga:
    pasutijums = models.OneToOneField(Pasutijums, to_field="id", on_delete=models.CASCADE, null=False,
                                   verbose_name="pasūtījums")

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return self.nosaukums

    # Lai administratoru lapā modeļa nosaukums parādās akurāti:
    class Meta:
        verbose_name = "Bilžu galerija"
        verbose_name_plural = "Bilžu galerijas"

    # Galerijas ieraksta izdzēšanas gadījumā ir jāizdzēš galerijas mapīte ar visām galerijas bildēm:
    @receiver(post_delete)
    def izdzest_galerijas_mapi(instance, *args, **kwargs):
        if type(instance) == BilzuGalerija:
            pasutijums = Pasutijums.objects.get(id=int(str(instance.pasutijums)))
            lietotajs = pasutijums.lietotajs
            lietotaja_profila_mapes_cels = lietotaja_profila_bildes_cels(lietotajs, filename="").split("/")[0]
            # Tiek izdzēsta bilžu galerijas mapīte:
            try:
                bilzu_galerija = str(MEDIA_ROOT) + "/" + lietotaja_profila_mapes_cels + "/" + str(
                    instance.id) + "_" + str(
                    instance.nosaukums)
                shutil.rmtree(bilzu_galerija)
            except:
                pass

    # Izvada cik dienas ir palikušas līdz galerijas izdzēšanai (30 dienas no galerrijas izveidošanas datuma):
    @property
    def dienas_lidz_galerijas_dzesanai(self):
        dienas_lidz = str(self.izveidosanas_datums.date() - date.today() + timedelta(days=30)).split(" ", 1)[0]
        return dienas_lidz


# Bilžu modelis:
class Bilde(models.Model):
    id = models.AutoField(primary_key=True)

    # Vieta, kur augšupielādēs bildi:
    atrasanas_vieta = models.CharField(max_length=300, null=True, verbose_name="atrašanās vieta")

    # Ārējā atslēga:
    bilzu_galerija = models.ForeignKey(BilzuGalerija, to_field="id", on_delete=models.CASCADE,
                                       verbose_name="bilžu galerija", null=False)
    lietotajs = models.ForeignKey(Lietotajs, to_field="epasts", on_delete=models.CASCADE, verbose_name="lietotājs")

    fails = models.ImageField(upload_to=bilzu_galerijas_cels, max_length=400)

    # Lai administratoru lapā modeļa nosaukums parādās akurāti:
    class Meta:
        verbose_name = "Bilde"
        verbose_name_plural = "Bildes"

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return str(self.id)

    # Bildes ieraksta izdzēšanas gadījumā ir jāizdzēš bilde no galerijas mapītes:
    @receiver(post_delete)
    def izdzest_galerijas_mapi(instance, *args, **kwargs):
        if type(instance) == Bilde:
            # Tiek izdzēsta bilde no galerijas mapītes:
            try:
                galerijas_bilde = str(MEDIA_ROOT) + "/" + str(instance.fails)
                os.remove(galerijas_bilde)
            except:
                pass

    # Pēc ieraksta saglabāšanas izdzēš bildes atrašanās vietas lauku, jo tas vairs nav vajadzīgs un bilžu galerijai pārmaina datumu uz tagadējo datumu un laiku:
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Bilde.objects.filter(id=self.id).update(atrasanas_vieta=None)
        BilzuGalerija.objects.filter(id=self.bilzu_galerija.id).update(izveidosanas_datums=timezone.now())
