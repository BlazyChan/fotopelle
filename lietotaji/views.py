from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Pieslēgšanās (ar visu autentifikāciju):
def pieslegties(request):
    if request.method == "POST":
        epasts = request.POST['epasts']
        parole = request.POST['parole']
        lietotajs = authenticate(request, username=epasts, password=parole)
        if lietotajs is not None:
            login(request, lietotajs)
            # Veiksmīgas pieslēgšanās gadījumā - lietotāju aizved uz norādīto lapu un izvada ziņu:
            #messages.success("Laupni lūdzam {}!".format(lietotajs.vards))
            return render(request, 'pasutit.html', {})
        else:
            # Neveiksmīgas pieslēgšanās gadījumā izvada kļūdu:
            messages.info(request, "Epasts vai parole tika ievadīta nepareizi, lūdzu mēģiniet vēlreiz!")
            return render(request, 'pieslegties.html', {})
    else:
        return render(request, 'pieslegties.html', {})


# Reģistrācija:
def registreties(request):
    return render(request, 'registreties.html', {})


# Izrakstīšanās:
def izrakstities(request):
    return render(request, 'izrakstities.html', {})
