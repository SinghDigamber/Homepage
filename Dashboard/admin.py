from django.contrib import admin
from .models import PlanetaKino, keyValue


class PlanetaKinoAdmin(admin.ModelAdmin):
    list_display = ('title', 'posterIMG', 'href', 'date', 'inTheater')
    list_filter = ('inTheater',)
admin.site.register(PlanetaKino, PlanetaKinoAdmin)

class keyValueAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
admin.site.register(keyValue, keyValueAdmin)