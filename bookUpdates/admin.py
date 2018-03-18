from django.contrib import admin
from .models import chapters

# Register your models here.
class ChapterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'href', 'datetime', 'title']}),
    ]
admin.site.register(chapters, ChapterAdmin)