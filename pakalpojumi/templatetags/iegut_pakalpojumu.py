from django import template

register = template.Library()


# Izvada pakalpojumu balstoties pēc tā indeksa pakalpojumu sarakstā:
@register.filter(name="iegut_pakalpojumu")
def iegut_pakalpojumu(pakalpojuma_saraksts, i):
    try:
        return pakalpojuma_saraksts[int(i)]
    except:
        return None
