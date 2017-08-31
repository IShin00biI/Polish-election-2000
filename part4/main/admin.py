from django.contrib import admin
from django.db.models import Sum

from .models import Country, Voivodeship, District, Commune
from .dictionaries import *


def annotation_getters(fields, field_names):
    result = []

    for field in fields:
        result.append(lambda obj, field=field: getattr(obj, field))
        result[-1].short_description = field_names[field]
        result[-1].admin_order_field = field

    return result


def candidate_annotation_getters():
    return annotation_getters(candidates, candidate_names)


def static_stat_annotation_getters():
    return annotation_getters(static_stats, stat_names)


class ContainerAndChildAreaInline(admin.TabularInline):
    class Meta:
        abstract = True

    annotation_prefix = ''

    def get_queryset(self, request):
        qs = super(ContainerAndChildAreaInline, self).get_queryset(request)
        for field in candidates + static_stats:
            qs = qs.annotate(**{field: Sum(self.annotation_prefix + field)})
        return qs

    readonly_fields = tuple(static_stat_annotation_getters()) + ('valid', 'given') \
                      + tuple(candidate_annotation_getters())


class DistrictInline(ContainerAndChildAreaInline):
    model = District
    extra = 1


class VoivodeshipInline(ContainerAndChildAreaInline):
    model = Voivodeship
    extra = 1


class CommuneInline(admin.TabularInline):
    model = Commune
    extra = 1


class ContainerAreaAdmin(admin.ModelAdmin):
    class Meta:
        abstract = True

    annotation_prefix = ''

    # Nie byłem w stanie sprawić, żeby rubryki valid i given były sortowalne
    list_display = ['pk'] + static_stat_annotation_getters() + ['valid', 'given']
    readonly_fields = tuple(static_stat_annotation_getters()) \
                      + tuple(candidate_annotation_getters()) + ('valid', 'given')

    def get_queryset(self, request):
        qs = super(ContainerAreaAdmin, self).get_queryset(request)
        for field in candidates + static_stats:
            qs = qs.annotate(**{field: Sum(self.annotation_prefix + field)})
        return qs


class CountryAdmin(ContainerAreaAdmin):
    inlines = [VoivodeshipInline]
    search_fields = ['pk']
    annotation_prefix = 'voivodeship__district__commune__'


class VoivodeshipAdmin(ContainerAreaAdmin):
    inlines = [DistrictInline]
    search_fields = ['pk']
    annotation_prefix = 'district__commune__'


class DistrictAdmin(ContainerAreaAdmin):
    inlines = [CommuneInline]
    annotation_prefix = 'commune__'


class CommuneAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'id') + tuple(stats)


VoivodeshipInline.annotation_prefix = VoivodeshipAdmin.annotation_prefix
DistrictInline.annotation_prefix = DistrictAdmin.annotation_prefix


admin.site.register(Country, CountryAdmin)
admin.site.register(Voivodeship, VoivodeshipAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Commune, CommuneAdmin)
