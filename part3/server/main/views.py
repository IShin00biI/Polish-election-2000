from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.db.models import Q, Sum
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Country, Voivodeship, District, Commune
from .dictionaries import *
from .forms import *


@require_POST
@csrf_exempt
def login_view(request, username):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        response = HttpResponse("OK")
    else:
        response = HttpResponse("DENIED")

    response["Access-Control-Allow-Origin"] = "*"
    return response


def search_view(request):
    phrase = request.GET.get('search')
    if phrase:
        if phrase.isdigit():
            results = Commune.objects.filter(Q(name__icontains=phrase) | Q(id=phrase))
        else:
            results = Commune.objects.filter(name__icontains=phrase)

        result_dict = {}
        for result in results:
            result_dict[result.pk] = result.__str__()

        response = JsonResponse(result_dict)

    else:
        response = HttpResponse("INVALID")
        response['status'] = 400

    response["Access-Control-Allow-Origin"] = "*"
    return response


# area view abstract
def area(request, area_class, pk):
    area = get_object_or_404(area_class, pk=pk)
    children = area.children()
    query_prefix = area.query_prefix()

    # preparing queries
    cand_query = {}
    stat_query = {}
    if children or query_prefix:
        for field in candidates:
            cand_query[field] = Sum(query_prefix + field)
        for field in static_stats:
            stat_query[field] = Sum(query_prefix + field)

    # fetching area results
    if children:
        cand_results = children.aggregate(**cand_query)
        stat_results = children.aggregate(**stat_query)
    else:
        cand_results = {}
        stat_results = {}
        for field in candidates:
            cand_results[field] = getattr(area, field)
        for field in static_stats:
            stat_results[field] = getattr(area, field)

    stat_results['valid'] = 0
    for cand in candidates:
        stat_results['valid'] += cand_results[cand]
    stat_results['given'] = stat_results['valid'] + stat_results['invalid']

    # swapping key names
    for stat in stats:
        stat_results[stat_names[stat]] = stat_results.pop(stat)

    # fetching children results
    if query_prefix:
        children = children.annotate(**stat_query).annotate(**cand_query)

    # repacking children results to a dictionary
    children_results = {}
    for child in children:
        child_results = {}
        for stat in static_stats:
            child_results[stat_names[stat]] = getattr(child,stat)

        child_results[stat_names['valid']] = 0
        for cand in candidates:
            child_results[stat_names['valid']] += getattr(child, cand)
        child_results[stat_names['given']] = \
            child_results[stat_names['valid']] + child_results[stat_names['invalid']]
        children_results[child.pk] = child_results

    response = JsonResponse ({
        'area': area.__str__(),
        'stats': stat_results,
        'candidates': cand_results,
        'children': children_results,
        'child_type': area.child_name(),
        'child_name': area_names[area.child_name()],
        'child_name_plural': area_names_p[area.child_name()],
        'stat_list': [ stat_names[stat] for stat in stats ],
        'candidate_names': candidate_names,
        'parent_type': area.parent_name(),
        'parent': (area.parent().pk if area.parent() else ''),
        'parent_name_full': (area.parent().__str__() if area.parent() else '')
    })
    response["Access-Control-Allow-Origin"] = "*"
    return response


def index(request):
    return area(request, Country, 'Polska')


def voivodeship(request, pk):
    return area(request, Voivodeship, pk)


def district(request, pk):
    return area(request, District, pk)


@csrf_exempt
def commune(request, pk):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            commune = get_object_or_404(Commune, pk=pk)
            commune_form = CommuneForm(request.POST, instance=commune)
            if commune_form.is_valid():
                commune_form.save()
                response = HttpResponse("OK")
            else:
                response = HttpResponse("INVALID")
                response['status'] = 400
        else:
            response = HttpResponse("DENIED")
            response['status'] = 401

        response["Access-Control-Allow-Origin"] = "*"
        return response

    else:
        return area(request, Commune, pk)
