from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Voivodeship, District, Commune


candidates = {
    'grabowski': 'crimson',
    'ikonowicz': 'blue',
    'kalinowski': 'yellow',
    'korwin': 'green',
    'krzaklewski': 'purple',
    'kwasniewski': 'pink',
    'lepper': 'brown',
    'lopuszanski': 'darkcyan',
    'olechowski': 'blueviolet',
    'pawlowski': 'greenyellow',
    'walesa': 'fuchsia',
    'wilecki': 'coral'
}


statistics = {
    'subareas': 'Obwody',
    'people': 'Uprawnieni',
    'cards': 'Karty wydane',
    'given': 'Głosy oddane',
    'valid': 'Głosy ważne',
    'invalid': 'Głosy nieważne'
}


def login(request):
    if (request.user.is_authenticated):
        return HttpResponse("Hi, %s!" % request.user.username)
    else:
        return HttpResponse("Hi, nobody!")


def index(request):
    return HttpResponse("Index")


def voivodeship(request, pk):
    voivodeship = get_object_or_404(Voivodeship, pk=pk)
    return render(request, 'main/voivodeship.html',
                  {'area': voivodeship, 'candidates': candidates, 'statistics': statistics})


def district(request, pk):
    return HttpResponse("Okręg")


def commune(request, pk):
    return HttpResponse("Gmina")
