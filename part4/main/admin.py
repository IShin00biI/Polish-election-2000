from django.contrib import admin

from .models import Country, Voivodeship, District, Commune
from .dictionaries import *


class VoivodeshipInline(admin.TabularInline):
    model = Voivodeship
    extra = 1


class DistrictInline(admin.TabularInline):
    model = District
    extra = 1


class CommuneInline(admin.TabularInline):
    model = Commune
    extra = 1


class CountryAdmin(admin.ModelAdmin):
    inlines = [VoivodeshipInline]
    search_fields = ['pk']


class VoivodeshipAdmin(admin.ModelAdmin):
    inlines = [DistrictInline]
    search_fields = ['pk']


class DistrictAdmin(admin.ModelAdmin):
    inlines = [CommuneInline]


class CommuneAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'id') + tuple(stats)

admin.site.register(Country, CountryAdmin)
admin.site.register(Voivodeship, VoivodeshipAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Commune, CommuneAdmin)
