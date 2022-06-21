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

    # Pārveido tekstu, kas ir virs tabulas administratora lapā:
    def changelist_view(self, request, extra_context=None):
        virsraksts = {"title": "Atlasiet pasūtījumu vai vairākus pasūtījumus, lai tos mainītu"}
        return super().changelist_view(request, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs jauna ieraksta izveides laukiem administratora lapā:
    def add_view(self, request, form_url='', extra_context=None):
        virsraksts = {"title": "Pievienot jaunu pasūtījumu"}
        return super().add_view(request, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs ieraksta rediģēšanas laukiem administratora lapā:
    def change_view(self, request, object_id, form_url='', extra_context=None):
        virsraksts = {"title": "Rediģēt pasūtījuma datus"}
        return super().change_view(request, object_id, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas atrodas dzēšanas apstiprināšanas administratora lapā:
    def delete_view(self, request, object_id, extra_context=None):
        nosaukums = "pasūtījumu"
        virsraksts = {"title": "Vai esat pārliecināts, ka vēlaties dzēst šo " + nosaukums + "?", "object_name": nosaukums}
        return super().delete_view(request, object_id, extra_context=virsraksts)


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

    # Pārveido tekstu, kas ir virs tabulas administratora lapā:
    def changelist_view(self, request, extra_context=None):
        virsraksts = {"title": "Atlasiet pakalpojuma veidu vai vairākus pakalpojuma veidus, lai tos mainītu"}
        return super().changelist_view(request, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs jauna ieraksta izveides laukiem administratora lapā:
    def add_view(self, request, form_url='', extra_context=None):
        virsraksts = {"title": "Pievienot jaunu pakalpojuma veidu"}
        return super().add_view(request, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs ieraksta rediģēšanas laukiem administratora lapā:
    def change_view(self, request, object_id, form_url='', extra_context=None):
        virsraksts = {"title": "Rediģēt pakalpojuma veida datus"}
        return super().change_view(request, object_id, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas atrodas dzēšanas apstiprināšanas administratora lapā:
    def delete_view(self, request, object_id, extra_context=None):
        nosaukums = "pakalpojuma veidu"
        virsraksts = {"title": "Vai esat pārliecināts, ka vēlaties dzēst šo " + nosaukums + "?", "object_name": nosaukums}
        return super().delete_view(request, object_id, extra_context=virsraksts)


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

    # Pārveido tekstu, kas ir virs tabulas administratora lapā:
    def changelist_view(self, request, extra_context=None):
        virsraksts = {"title": "Atlasiet bilžu galeriju vai vairākas bilžu galerijas, lai tās mainītu"}
        return super().changelist_view(request, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs jauna ieraksta izveides laukiem administratora lapā:
    def add_view(self, request, form_url='', extra_context=None):
        virsraksts = {"title": "Pievienot jaunu bilžu galeriju"}
        return super().add_view(request, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs ieraksta rediģēšanas laukiem administratora lapā:
    def change_view(self, request, object_id, form_url='', extra_context=None):
        virsraksts = {"title": "Rediģēt bilžu galerijas datus"}
        return super().change_view(request, object_id, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas atrodas dzēšanas apstiprināšanas administratora lapā:
    def delete_view(self, request, object_id, extra_context=None):
        nosaukums = "bilžu galeriju"
        virsraksts = {"title": "Vai esat pārliecināts, ka vēlaties dzēst šo " + nosaukums + "?", "object_name": nosaukums}
        return super().delete_view(request, object_id, extra_context=virsraksts)


admin.site.register(BilzuGalerija, BilzuGalerijaAdmin)


# Bildes (darbības un ierakstu atrādīšana administratoru panelī):
class BildeAdmin(admin.ModelAdmin):
    list_display = ["id", "fails", "bilzu_galerija_id", "lietotajs"]
    ordering = ["id"]
    actions = [izdzest_bildes]

    # Izdzēš noklusēto/jau gatavo darbību:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    # Pārveido tekstu, kas ir virs tabulas administratora lapā:
    def changelist_view(self, request, extra_context=None):
        virsraksts = {"title": "Atlasiet bildi vai vairākas bildes, lai tās mainītu"}
        return super().changelist_view(request, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs jauna ieraksta izveides laukiem administratora lapā:
    def add_view(self, request, form_url='', extra_context=None):
        virsraksts = {"title": "Pievienot jaunu bildi"}
        return super().add_view(request, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs ieraksta rediģēšanas laukiem administratora lapā:
    def change_view(self, request, object_id, form_url='', extra_context=None):
        virsraksts = {"title": "Rediģēt bildes datus"}
        return super().change_view(request, object_id, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas atrodas dzēšanas apstiprināšanas administratora lapā:
    def delete_view(self, request, object_id, extra_context=None):
        nosaukums = "bildi"
        virsraksts = {"title": "Vai esat pārliecināts, ka vēlaties dzēst šo " + nosaukums + "?", "object_name": nosaukums}
        return super().delete_view(request, object_id, extra_context=virsraksts)


admin.site.register(Bilde, BildeAdmin)
