from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
import os
import shutil
from fotopelle.settings import MEDIA_ROOT


# Izveido un izvada unikālu lietotāja mapīti un ievieto tur bildi ar orģinālo faila (bildes) nosaukumu:
def lietotaja_profila_bildes_cels(instance, filename):
    return 'lietotajs_{0}/profila_bilde/{1}'.format(instance.epasts.replace("@", "_"), filename)


# Parasta lietotāja pārvaldnieks (manager):
class LietotajaParvaldnieks(BaseUserManager):
    # Izveido parastu lietotāju:
    def create_user(self, epasts, password, **citi_lauki):
        if not epasts:
            raise ValueError('Lietotājam ir nepieciešama epasta adrese!')
        if not password:
            raise ValueError('Lietotājam ir nepieciešama parole!')
        lietotajs = self.model(
            epasts=self.normalize_email(epasts),
            **citi_lauki
        )
        lietotajs.set_password(password)
        lietotajs.save(using=self._db)
        return lietotajs

    # Izveido administratoru (ar visām atļaujām):
    def create_superuser(self, epasts, password=None):
        lietotajs = self.create_user(
            epasts=epasts,
            password=password
        )
        lietotajs.is_active = True
        lietotajs.is_admin = True
        lietotajs.is_staff = True
        lietotajs.is_superuser = True
        lietotajs.save()
        return lietotajs


# Parasta lietotāja modelis:
class Lietotajs(AbstractBaseUser):
    epasts = models.EmailField(max_length=64, primary_key=True)

    # Lauks, kurš tiks izmantots lai ieietu profilā:
    USERNAME_FIELD = 'epasts'

    # Django nepieciešamie lauki:
    is_active = models.BooleanField(default=True)  # Var pieslēgties
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Piekļuve administratora vietnei
    is_superuser = models.BooleanField(default=False)  # Ir visas atļaujas (tās specifiski nenorādot)

    # Šie vēlāk būs nepieciešamie lauki:
    vards = models.CharField(max_length=32)
    uzvards = models.CharField(max_length=32)
    telefona_numurs = models.CharField(max_length=15)

    # Pārējie lauki:
    profila_bilde = models.ImageField(default='profila_bilde/noklusējuma_profila_bilde.png',
                                      upload_to=lietotaja_profila_bildes_cels)

    # Te jānorāda lietotāja pārvaldnieks (manager):
    objects = LietotajaParvaldnieks()

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return str(self.epasts) + " - " + str(self.vards) + " " + str(self.uzvards)

    # Izvada lietotāja atļaujas:
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# Fotogrāfa (lietotājs ar papildus lauku un citām atļaujām) modelis:
class Fotografs(models.Model):
    lietotajs = models.OneToOneField(Lietotajs, to_field="epasts", on_delete=models.CASCADE, primary_key=True)
    # Papildus lauki fotogrāfam:
    apraksts = models.TextField()

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return str(self.lietotajs)


# Jaunas lietotāja profila bildes pievienošanas gadījumā ir jāizdzēš vecā profila bilde:
@receiver(pre_save, sender=Lietotajs)
def jauna_profila_bilde(sender, instance, *args, **kwargs):
    try:
        veca_bilde = Lietotajs.object.get(epasts=instance.epasts).profila_bilde.path
        try:
            jauna_bilde = instance.profila_bilde.path
        except:
            jauna_bilde = None

        if jauna_bilde != veca_bilde and str(Lietotajs.object.get(epasts=instance.epasts).profila_bilde) != "profila_bilde/noklusējuma_profila_bilde.png":
            if os.path.exists(veca_bilde):
                os.remove(veca_bilde)
    except:
        pass


# Lietotāja izdzēšanas gadījumā ir jāizdzēš vecā profila bildes mapīte:
@receiver(pre_delete, sender=Lietotajs)
def izdzest_mapi(sender, instance, *args, **kwargs):
    try:
        shutil.rmtree(str(MEDIA_ROOT) + "/" + lietotaja_profila_bildes_cels(instance, filename="").split("/")[0])
    except:
        pass
