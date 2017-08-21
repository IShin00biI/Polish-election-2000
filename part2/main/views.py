from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Voivodeship, District, Commune
from .dictionaries import stats, candidates, candidate_colors


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
                  {'area': voivodeship, 'candidates': candidates,
                   'stats': stats, 'candidate_colors': candidate_colors})


def district(request, pk):
    return HttpResponse("Okręg")


def commune(request, pk):
    return HttpResponse("Gmina")
