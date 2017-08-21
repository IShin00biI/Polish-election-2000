from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Country, Voivodeship, District, Commune
from .dictionaries import *


def login(request):
    if (request.user.is_authenticated):
        return HttpResponse("Hi, %s!" % request.user.username)
    else:
        return HttpResponse("Hi, nobody!")


# area view abstract
def area(request, pk, area_type, child_name):
    area = get_object_or_404(area_type, pk=pk)
    return render(request, 'main/area.html',
                 {'area': area, 'child_name': child_name, **dictionaries})


def index(request):
    return area(request, 'Polska', Country, 'voivodeship')


def voivodeship(request, pk):
    return area(request, pk, Voivodeship, 'district')


def district(request, pk):
    return area(request, pk, District, 'commune')


def commune(request, pk):
    return area(request, pk, Commune, '')
