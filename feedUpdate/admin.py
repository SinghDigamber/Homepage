from django.contrib import admin
from .models import feedUpdate

# Register your models here.
class feedUpdateAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'title', 'href')

admin.site.register(feedUpdate, feedUpdateAdmin)
