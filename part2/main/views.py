from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

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
    phrase = request.GET.get('search')
    if phrase:
        if phrase.isdigit():
            results = Commune.objects.filter(Q(name__icontains=phrase) | Q(id=phrase))
        else:
            results = Commune.objects.filter(name__icontains=phrase)
        return render(request, 'main/search.html', {'results': results, 'search': phrase})
    else:
        return HttpResponseRedirect(reverse('main:index'))


# area view abstract
def area(request, pk, area_type, child_name, commune_form=None, error_msg=None):
    area = get_object_or_404(area_type, pk=pk)
    return render(request, 'main/area.html',
                 {'area': area, 'child_name': child_name,
                  'commune_form': commune_form, 'error_msg': error_msg, **dictionaries})


def index(request):
    return area(request, 'Polska', Country, 'voivodeship')


def voivodeship(request, pk):
    return area(request, pk, Voivodeship, 'district')


def district(request, pk):
    return area(request, pk, District, 'commune')


def commune(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            commune = get_object_or_404(Commune, pk=pk)
            commune_form = CommuneForm(request.POST, instance=commune)
            if commune_form.is_valid():
                commune_form.save()
                return HttpResponseRedirect(reverse('main:commune', kwargs={'pk': pk}))
            else:
                return area(request, pk, Commune, 'commune',
                            commune_form=commune_form, error_msg='Dane są niepoprawne!')
        else:
            commune = get_object_or_404(Commune, pk=pk)
            commune_form = CommuneForm(instance=commune)
            return area(request, pk, Commune, 'commune', commune_form=commune_form)
    else:
        return area(request, pk, Commune, 'commune')
