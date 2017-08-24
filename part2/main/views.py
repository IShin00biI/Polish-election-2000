from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Sum

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

'''
# area view abstract
def areaold(request, pk, area_type, child_name, commune_form=None, error_msg=None):
    area = get_object_or_404(area_type, pk=pk)
    return render(request, 'main/area.html',
                 {'area': area, 'child_name': child_name,
                  'commune_form': commune_form, 'error_msg': error_msg, **dictionaries})
'''


# area view abstract
def area(request, area_class, pk, error_msg='', commune_form=None):
    area = get_object_or_404(area_class, pk=pk)
    children = area.children()
    query_prefix = area.query_prefix()

    query = {}
    if children or query_prefix:
        for field in candidates + static_stats:
            query = {**query, field: Sum(query_prefix + field)}

    if children:
        results = children.aggregate(**query)
    else:
        results = {}
        for field in candidates + static_stats:
            results = { **results, field: getattr(area, field) }

    results['valid'] = 0
    for cand in candidates:
        results['valid'] += results[cand]
    results['given'] = results['valid'] + results['invalid']

    if query_prefix:
        children = children.annotate(**query)

    return render(request, 'main/area.html',
                  { 'area': area,
                    'results': results,
                    'children': children,
                    'child_name': area.child_name(),
                    'error_msg': error_msg,
                    'commune_form': commune_form})


def index(request):#(request):
    return area(request, Country, 'Polska')


def voivodeship(request, pk):#(request, pk):
    return area(request, Voivodeship, pk)


def district(request, pk):#(request, pk):
    return area(request, District, pk)


def commune(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            commune = get_object_or_404(Commune, pk=pk)
            commune_form = CommuneForm(request.POST, instance=commune)
            if commune_form.is_valid():
                commune_form.save()
                return HttpResponseRedirect(reverse('main:commune', kwargs={'pk': pk}))
            else:
                return area(request, pk,
                            Commune, error_msg='Dane są niepoprawne!',
                            commune_form=commune_form)
        else:
            commune = get_object_or_404(Commune, pk=pk)
            commune_form = CommuneForm(instance=commune)
            return area(request, pk, Commune, commune_form=commune_form)
    else:
        return area(request, pk, Commune)
