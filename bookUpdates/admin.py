from django.contrib import admin
from .models import bookUpdate

# Register your models here.
class bookUpdateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'href', 'datetime', 'title']}),
    ]


admin.site.register(bookUpdate, bookUpdateAdmin)

