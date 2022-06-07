from django import template

register = template.Library()


# Izvada pasūtījumu balstoties pēc tā indeksa pasūtījumu sarakstā:
@register.filter(name="iegut_pasutijumu")
def iegut_pasutijumu(pasutijuma_saraksts, i):
    try:
        return pasutijuma_saraksts[int(i)]
    except:
        return None
