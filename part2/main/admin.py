from django.contrib import admin

from .models import Country, Voivodeship, District, Commune

# Register your models here.
admin.site.register(Country)
admin.site.register(Voivodeship)
admin.site.register(District)
admin.site.register(Commune)
