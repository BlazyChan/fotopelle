from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from .forms import RegistracijasVeidlapa, ProfilaRedigesanasVeidlapa
from django.views.generic.edit import UpdateView, CreateView
from .models import Lietotajs
from django.contrib.auth.forms import UserChangeForm


# Pieslēgšanās (ar visu autentifikāciju):
def pieslegties(request):
    if request.method == "POST":
        epasts = request.POST['epasts']
        parole = request.POST['parole']
        lietotajs = authenticate(request, username=epasts, password=parole)
        if lietotajs is not None:
            login(request, lietotajs)
            # Veiksmīgas pieslēgšanās gadījumā - lietotāju aizved uz norādīto lapu un izvada ziņu:
            messages.success(request, "Laipni lūdzam {}!".format(lietotajs.vards))
            return redirect('sākumlapa')
        else:
            # Neveiksmīgas pieslēgšanās gadījumā izvada kļūdu:
            messages.info(request, "Epasts vai parole tika ievadīta nepareizi, lūdzu mēģiniet vēlreiz!")
            return redirect('pieslēgties')
    else:
        return render(request, 'pieslegties.html', {})


# Reģistrācija:
def registreties(request):
    if request.method == "POST":
        form = RegistracijasVeidlapa(request.POST)
        if form.is_valid():
            form.save()
            epasts = form.cleaned_data['epasts']
            parole = form.cleaned_data['password1']
            lietotajs = authenticate(request, username=epasts, password=parole)
            login(request, lietotajs)
            # Veiksmīgas reģistrācijas gadījumā - lietotāju aizved uz norādīto lapu un izvada ziņu:
            messages.success(request, "Jūsu profils tika veiksmīgi izveidots!")
            return redirect('sākumlapa')
    else:
        form = RegistracijasVeidlapa()
    return render(request, 'registreties.html', {"form": form})


# Izrakstīšanās:
def izrakstities(request):
    logout(request)
    return redirect('/')


# Profila rediģēšana:
class RedigetProfilu(SuccessMessageMixin, UpdateView):
    form_class = ProfilaRedigesanasVeidlapa
    model = Lietotajs
    template_name = "rediget_profilu.html"
    success_url = "/rediget_profilu/"
    success_message = "Jūsu profila izmaiņas tika veiksmīgi saglabātas!"

    def get_object(self):
        return self.request.user
