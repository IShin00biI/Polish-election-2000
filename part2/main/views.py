from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Voivodeship, District, Commune


candidates = [
    'grabowski'
    'ikonowicz',
    'kalinowski',
    'korwin',
    'krzaklewski',
    'kwasniewski',
    'lepper',
    'lopuszanski',
    'olechowski',
    'pawlowski',
    'walesa',
    'wilecki'
]


def login(request):
    if (request.user.is_authenticated):
        return HttpResponse("Hi, %s!" % request.user.username)
    else:
        return HttpResponse("Hi, nobody!")


def index(request):
    return HttpResponse("Index")


def voivodeship(request, pk):
    #return HttpResponse("Województwo")
    voivodeship = get_object_or_404(Voivodeship, pk=pk)
    return render(request, 'main/voivodeship.html', {'area': voivodeship, 'candidates': candidates})


def district(request, pk):
    return HttpResponse("Okręg")


def commune(request, pk):
    return HttpResponse("Gmina")
