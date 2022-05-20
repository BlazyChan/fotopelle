from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
        lietotajs.save()
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
    profila_bilde = models.ImageField(default='profila_bildes/noklusējuma_profila_bilde.png',
                                      upload_to='profila_bildes/')

    # Te jānorāda lietotāja pārvaldnieks (manager):
    object = LietotajaParvaldnieks()

    # Tas ko izvada, ja izsauc šī moduļa instanci:
    def __str__(self):
        return self.epasts

    # Izvada lietotāja atļaujas:
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# Fotogrāfa (lietotājs ar papildus lauku un citām atļaujām) modelis:
class Fotografs(models.Model):
    lietotajs = models.OneToOneField(Lietotajs, on_delete=models.CASCADE, primary_key=True)

    # Papildus lauki fotogrāfam:
    apraksts = models.TextField()
