from django.shortcuts import render

# Lapa, kur lietotājs var veikt pasūtījumus, jeb pasūtīt pakalpojumus:
def pasutit(request):
    return render(request, 'pasutit.html', {})