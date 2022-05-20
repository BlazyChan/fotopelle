from django.shortcuts import render


# Sākumlapa (pirmā lapa, ko redz atverot mājaslapu):
def sakumlapa(request):
    return render(request, 'sakumlapa.html', {})


# Lapa, kur lietotājs var veikt pasūtījumus, jeb pasūtīt pakalpojumus:
def pasutit(request):
    return render(request, 'pasutit.html', {})
