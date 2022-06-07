from django import template

register = template.Library()


# Izvada normalizētu telefona numuru (lai telefona numuri būtu vienotā stilā/formātā):
@register.filter(name="izdailot_telefona_numuru")
def izdailot_telefona_numuru(telefona_numurs):
    try:
        telefona_numurs = telefona_numurs.replace("-","")
        if "+371 " in telefona_numurs:
            telefona_numurs = telefona_numurs[0:5] + telefona_numurs[4:-1].replace(" ","")
        else:
            telefona_numurs = telefona_numurs.replace(" ","")
        return telefona_numurs
    except:
        return None
