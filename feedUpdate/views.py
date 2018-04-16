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
        header = "Forced!"
        multibook = True

        try:
            if self.kwargs['feeds'] != "":
                header = self.kwargs['feeds']

                items = self.kwargs['feeds']
                items = items.split("+")
                if len(items) == 1:
                    multibook = False
        except KeyError:
            items = feedUpdate.feeds.keys()

        items = feedUpdate.multilist(items)
        items = sorted(items, key=lambda feedUpdate: str(feedUpdate.datetime), reverse=True)

        return {
            'title': header,
            'chapters': items,
            'multibook': multibook
        }


class feedUpdateIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "list"

    def get_queryset(self):
        header = "Обновления"
        multibook = True

        try:
            if self.kwargs['feeds'] != "":
                header = self.kwargs['feeds']
                if len(header.split("+")) == 1:
                    multibook = False
                    header = feedUpdate.feeds[header]['title_full']
                feeds = list(feedUpdate.objects.filter(title__in=header.split("+")))
        except KeyError:
            feeds = list(feedUpdate.objects.all()[:42])

        return {
            'title': header,
            'chapters': feeds,
            'multibook': multibook,
        }

class feedUpdateCacheView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/cached.html"

    def get_queryset(self):
        feedUpdate.cache()

        return { }
