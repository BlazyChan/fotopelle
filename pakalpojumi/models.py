from django.db import models
from lietotaji.models import Lietotajs, Fotografs
from datetime import date, timedelta


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


# Pasūtījuma modelis:
class Pasutijums(models.Model):
    id = models.AutoField(primary_key=True)

    # Vai pakalpojums ir aktīvs vai pabeigts (statuss)?
    aktivs = models.BooleanField(default=True)

    # Automātiski izveidots datums:
    pasutijuma_veiktais_datums = models.DateTimeField(auto_now_add=True)

    pasutijuma_datums = models.DateField()
    pasutijuma_laiks = models.TimeField()

    apraksts = models.TextField(null=True)
    # Jāaprēķina:
    kopeja_cena = models.FloatField(null=True)

    # Ārējās atslēgas:
    lietotajs = models.ForeignKey(Lietotajs, to_field="epasts", on_delete=models.CASCADE)
    pakalpojuma_veids = models.ForeignKey(PakalpojumaVeids, to_field="nosaukums", on_delete=models.SET_NULL, null=True)
    fotografs = models.ForeignKey(Fotografs, to_field="lietotajs", on_delete=models.SET_NULL, null=True)

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return str(self.id) + "_" + str(self.pasutijuma_datums)


# Bilžu galerija
class BilzuGalerija(models.Model):
    id = models.AutoField(primary_key=True)
    nosaukums = models.CharField(max_length=128)
    izveidosanas_datums = models.DateTimeField(auto_now_add=True)

    # Ārējā atslēga:
    pasutijums = models.ForeignKey(Pasutijums, to_field="id", on_delete=models.CASCADE, null=False)

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return self.nosaukums

    # Izvada cik dienas ir palikušas līdz galerijas izdzēšanai (30 dienas no galerrijas izveidošanas datuma):
    @property
    def dienas_lidz_galerijas_dzesanai(self):
        dienas_lidz = str(self.izveidosanas_datums.date() - date.today() + timedelta(days=30)).split(" ", 1)[0]
        return dienas_lidz


# Bilžu modelis:
class Bilde(models.Model):
    id = models.AutoField(primary_key=True)

    # Vieta, kur augšupielādēs bildi:
    atrasanas_vieta = models.CharField(max_length=286, null=False)

    # Ārējā atslēga:
    bilzu_galerija = models.ForeignKey(BilzuGalerija, to_field="id", on_delete=models.CASCADE)
    lietotajs = models.ForeignKey(Lietotajs, to_field="epasts", on_delete=models.SET_NULL, null=True)

    fails = models.ImageField(upload_to=bilzu_galerijas_cels)

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return self.atrasanas_vieta
