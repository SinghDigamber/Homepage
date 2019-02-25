from django.contrib import admin
from .models import feed, feedUpdate

# Register your models here.
class feedUpdateAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'title', 'href')
    list_filter = ('title',)
admin.site.register(feedUpdate, feedUpdateAdmin)


class feedAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_full', 'emojis', 'filter', 'delay', 'href', 'href_title')
    list_filter = ('emojis',)
admin.site.register(feed, feedAdmin)