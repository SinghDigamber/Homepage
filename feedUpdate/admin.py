from django.contrib import admin
from .models import feedUpdate

# Register your models here.
class feedUpdateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'href', 'datetime', 'title']}),
    ]
admin.site.register(feedUpdate, feedUpdateAdmin)

