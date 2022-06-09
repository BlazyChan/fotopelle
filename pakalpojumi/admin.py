from django.contrib import admin
from .models import Pasutijums, PakalpojumaVeids, BilzuGalerija, Bilde


# Iespējamās darbības ar ierakstiem administratoru panelī:

# Pasūtījumu izdzēšana:
@admin.action(description="Izdzēst izvēlētos pasūtījumus")
def izdzest_pasutijumus(modeladmin, request, queryset):
    queryset.delete()


# Pakalpojumu veidu izdzēšana:
@admin.action(description="Izdzēst izvēlētos pakalpojuma veidus")
def izdzest_pakalpojuma_veidus(modeladmin, request, queryset):
    queryset.delete()


# Bilžu galeriju izdzēšana:
@admin.action(description="Izdzēst izvēlētās bilžu galerijas")
def izdzest_bilzu_galerijas(modeladmin, request, queryset):
    queryset.delete()


# Bilžu izdzēšana:
@admin.action(description="Izdzēst izvēlētās bildes")
def izdzest_bildes(modeladmin, request, queryset):
    queryset.delete()


# Deaktivizē pasūtījumu:
@admin.action(description="Deaktivizēt pasūtījumu")
def deaktivizet(modeladmin, request, queryset):
    queryset.update(aktivs=False)


# Aktivizē pasūtījumu:
@admin.action(description="Aktivizēt pasūtījumu")
def aktivizet(modeladmin, request, queryset):
    queryset.update(aktivs=True)


# Pasūtījumi (darbības un ierakstu atrādīšana administratoru panelī):
class PasutijumsAdmin(admin.ModelAdmin):
    list_display = ["id", "aktivs", "pakalpojuma_veids", "kopeja_cena", "pasutijuma_veiktais_datums", "lietotajs", "pasutijuma_datums", "pasutijuma_laiks"]
    ordering = ["id"]
    actions = [izdzest_pasutijumus, deaktivizet, aktivizet]

    # Izdzēš noklusēto/jau gatavo darbību:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


admin.site.register(Pasutijums, PasutijumsAdmin)


# Pasūtījumu veidi (darbības un ierakstu atrādīšana administratoru panelī):
class PakalpojumaVeidsAdmin(admin.ModelAdmin):
    list_display = ["nosaukums", "apraksts", "cena"]
    ordering = ["nosaukums"]
    actions = [izdzest_pakalpojuma_veidus]

    # Izdzēš noklusēto/jau gatavo darbību:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


admin.site.register(PakalpojumaVeids, PakalpojumaVeidsAdmin)


# Bilžu galerijas (darbības un ierakstu atrādīšana administratoru panelī):
class BilzuGalerijaAdmin(admin.ModelAdmin):
    list_display = ["id", "nosaukums", "izveidosanas_datums", "pasutijums"]
    ordering = ["id"]
    actions = [izdzest_bilzu_galerijas]

    # Izdzēš noklusēto/jau gatavo darbību:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


admin.site.register(BilzuGalerija, BilzuGalerijaAdmin)


# Bildes (darbības un ierakstu atrādīšana administratoru panelī):
class BildeAdmin(admin.ModelAdmin):
    list_display = ["id", "fails", "bilzu_galerija", "lietotajs"]
    ordering = ["id"]
    actions = [izdzest_bildes]

    # Izdzēš noklusēto/jau gatavo darbību:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


admin.site.register(Bilde, BildeAdmin)
