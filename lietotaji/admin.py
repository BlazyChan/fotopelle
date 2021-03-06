from django.contrib import admin
from .models import Lietotajs, Fotografs
from django.contrib.auth.models import Group

# Izņem lieku saiti no administratora lapas:
admin.site.unregister(Group)


# Iespējamās darbības ar ierakstiem administratoru panelī:

# Lietotāju izdzēšana:
@admin.action(description="Izdzēst izvēlētos lietotājus")
def izdzest_lietotaju(modeladmin, request, queryset):
    queryset.delete()


# Norāda, ka lietotājs ir fotogrāfs (lietotājam piešķir fotogrāfa tiesības):
@admin.action(description="Piešķirt fotogrāfa tiesības")
def pieskirt_fotografa_tiesibas(modeladmin, request, queryset):
    for lietotajs in queryset:
        Fotografs.objects.create(lietotajs=lietotajs)


# Norāda, ka lietotājs nav fotogrāfs (lietotājam noņem fotogrāfa tiesības):
@admin.action(description="Noņemt fotogrāfa tiesības")
def nonemt_fotografa_tiesibas(modeladmin, request, queryset):
    for lietotajs in queryset:
        try:
            Fotografs.objects.get(lietotajs=lietotajs).delete()
        except:
            pass


# Deaktivizē lietotāju (lietotājs nevar pieslēgties):
@admin.action(description="Deaktivizēt lietotājus")
def deaktivizet(modeladmin, request, queryset):
    queryset.update(is_active=False)


# Aktivizē lietotāju (lietotājs var pieslēgties):
@admin.action(description="Aktivizēt lietotājus")
def aktivizet(modeladmin, request, queryset):
    queryset.update(is_active=True)


# Lietotājs (darbības un ierakstu atrādīšana administratoru panelī):
class LietotajsAdmin(admin.ModelAdmin):
    list_display = ["epasts", "is_active", "is_admin", "ir_fotografs", "vards", "uzvards", "telefona_numurs",
                    "last_login"]
    ordering = ["epasts"]
    actions = [izdzest_lietotaju, pieskirt_fotografa_tiesibas, nonemt_fotografa_tiesibas, deaktivizet, aktivizet]

    # Izdzēš noklusēto/jau gatavo darbību:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    # Pārveido tekstu, kas ir virs tabulas administratora lapā:
    def changelist_view(self, request, extra_context=None):
        virsraksts = {"title": "Atlasiet lietotāju vai vairākus lietotājus, lai tos mainītu"}
        return super().changelist_view(request, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs jauna ieraksta izveides laukiem administratora lapā:
    def add_view(self, request, form_url='', extra_context=None):
        virsraksts = {"title": "Pievienot jaunu lietotāju"}
        return super().add_view(request, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs ieraksta rediģēšanas laukiem administratora lapā:
    def change_view(self, request, object_id, form_url='', extra_context=None):
        virsraksts = {"title": "Rediģēt lietotāja datus"}
        return super().change_view(request, object_id, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas atrodas dzēšanas apstiprināšanas administratora lapā:
    def delete_view(self, request, object_id, extra_context=None):
        nosaukums = "lietotāju"
        virsraksts = {"title": "Vai esat pārliecināts, ka vēlaties dzēst šo " + nosaukums + "?", "object_name": nosaukums}
        return super().delete_view(request, object_id, extra_context=virsraksts)


admin.site.register(Lietotajs, LietotajsAdmin)


# Lietotājs (darbības un ierakstu atrādīšana administratoru panelī):
class FotografsAdmin(admin.ModelAdmin):
    list_display = ["lietotajs", "apraksts"]
    ordering = ["lietotajs"]
    actions = [nonemt_fotografa_tiesibas]

    # Izdzēš noklusēto/jau gatavo darbību:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    # Pārveido tekstu, kas ir virs tabulas administratora lapā:
    def changelist_view(self, request, extra_context=None):
        virsraksts = {"title": "Atlasiet fotogrāfu vai vairākus fotogrāfus, lai tos mainītu"}
        return super().changelist_view(request, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs jauna ieraksta izveides laukiem administratora lapā:
    def add_view(self, request, form_url='', extra_context=None):
        virsraksts = {"title": "Pievienot jaunu fotogrāfu"}
        return super().add_view(request, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas ir virs ieraksta rediģēšanas laukiem administratora lapā:
    def change_view(self, request, object_id, form_url='', extra_context=None):
        virsraksts = {"title": "Rediģēt fotogrāfa datus"}
        return super().change_view(request, object_id, form_url, extra_context=virsraksts)

    # Pārveido tekstu, kas atrodas dzēšanas apstiprināšanas administratora lapā:
    def delete_view(self, request, object_id, extra_context=None):
        nosaukums = "fotogrāfu"
        virsraksts = {"title": "Vai esat pārliecināts, ka vēlaties dzēst šo " + nosaukums + "?", "object_name": nosaukums}
        return super().delete_view(request, object_id, extra_context=virsraksts)


admin.site.register(Fotografs, FotografsAdmin)
