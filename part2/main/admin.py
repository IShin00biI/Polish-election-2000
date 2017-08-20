from django.contrib import admin

from .models import Voivodeship, District, Commune

# Register your models here.
admin.site.register(Voivodeship)
admin.site.register(District)
admin.site.register(Commune)
