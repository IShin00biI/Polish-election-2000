from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Country, Voivodeship, District, Commune
from .dictionaries import *
from .forms import *


def login_view(request, username):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:index'))
    else:
        if request.method == 'POST':
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
            else:
                return render(request, 'main/login.html', {'username': request.POST['username']})
        else:
            return render(request, 'main/login.html', {'username': ''})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def search_view(request):
    return HttpResponse("search")


# area view abstract
def area(request, pk, area_type, child_name, commune_form=None):
    area = get_object_or_404(area_type, pk=pk)
    return render(request, 'main/area.html',
                 {'area': area, 'child_name': child_name,
                  'commune_form': commune_form, **dictionaries})


def index(request):
    return area(request, 'Polska', Country, 'voivodeship')


def voivodeship(request, pk):
    return area(request, pk, Voivodeship, 'district')


def district(request, pk):
    return area(request, pk, District, 'commune')


def commune(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            commune_form = CommuneForm(request.POST)
            if commune_form.is_valid():
                commune_form.save()
                return HttpResponseRedirect(reverse('main:commune', pk))
        else:
            commune = get_object_or_404(Commune, pk=pk)
            commune_form = CommuneForm(instance=commune)
            return area(request, pk, Commune, 'commune', commune_form=commune_form)
    else:
        return area(request, pk, Commune, 'commune')
