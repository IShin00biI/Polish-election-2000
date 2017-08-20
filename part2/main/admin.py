from django.contrib import admin

from .models import County, Area, Commune

# Register your models here.
admin.site.register(County)
admin.site.register(Area)
admin.site.register(Commune)
