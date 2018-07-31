from django.shortcuts import render
from .models import feedUpdate
from django.views.generic import ListView
import socket
from django.shortcuts import redirect


class feedUpdateForceIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "list"

    def get_queryset(self):
        header = "Обновления: Forced"
        multibook = True

        try:
            if self.kwargs['feeds'] != "":
                header = self.kwargs['feeds']

                items = self.kwargs['feeds']
                items = items.split("+")
                if len(items) == 1:
                    multibook = False
                    header = feedUpdate.feeds[header]['title_full']
        except KeyError:
            items = feedUpdate.feeds.keys()

        items = feedUpdate.multilist(items)
        items = sorted(items, key=lambda feedUpdate: str(feedUpdate.datetime), reverse=True)

        return {
            'title': header,
            'items': items,
            'multibook': multibook
        }

class feedUpdateIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "list"

    def get_queryset(self):
        items_limit = 42
        header = "Обновления"
        multibook = True

        try:
            if self.kwargs['feeds'] != "":
                header = self.kwargs['feeds']
                if len(header.split("+")) == 1:
                    multibook = False
                    header = feedUpdate.feeds[header]['title_full']
                items = list(feedUpdate.objects.filter(title__in=self.kwargs['feeds'].split("+"))[:items_limit])
        except KeyError:
            items = list(feedUpdate.objects.all()[:items_limit])

        return {
            'title': header,
            'items': items,
            'multibook': multibook,
        }

# full feedUpdateIndexView copy except for number of items returned (420, not 42)
class feedUpdateIndexMoreView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "list"

    def get_queryset(self):
        items_limit = 420
        header = "Обновления"
        multibook = True

        try:
            if self.kwargs['feeds'] != "":
                header = self.kwargs['feeds']
                if len(header.split("+")) == 1:
                    multibook = False
                    header = feedUpdate.feeds[header]['title_full']
                items = list(feedUpdate.objects.filter(title__in=self.kwargs['feeds'].split("+"))[:items_limit])
        except KeyError:
            items = list(feedUpdate.objects.all()[:items_limit])

        return {
            'title': header,
            'items': items,
            'multibook': multibook,
        }

# TODO: fully remove accessing it by switching caching to shell script
class feedUpdateCacheView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/cached.html"

    def get_queryset(self):
        feedUpdate.cache()

        return { }
