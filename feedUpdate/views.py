from django.shortcuts import render
from .models import feedUpdate, feed
from django.views.generic import ListView
import socket
from django.shortcuts import redirect
from django.urls import reverse


class feedIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/feeds.html"
    context_object_name = "fromView"

    def get_queryset(self):
        header = "Ленты обновлений"

        items = feed.all()

        return {
            'title': header,
            'feeds': items,
        }


class feedUpdateIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "fromView"

    def get_queryset(self):
        items_limit = 42
        header = "Обновления"

        multibook = True  # check for multibook and creates items object with required feeds
        try:
            if self.kwargs['feeds'] != "force" and self.kwargs['feeds'] != "index":
                header = self.kwargs['feeds']
                items = header.split("+")
                if len(items) == 1:
                    multibook = False
                    # TODO: check if feeds exists and return error if not. Maybe KeyError is returned here?
                    try:
                        if feed.find(header).title_full:
                            header = feed.find(header).title_full
                        else:
                            header = feed.find(header).title
                    except KeyError:
                        header = "Header "+header+" does not exist"
                        items = []
            else:
                items = feed.keys()
                self.kwargs['mode'] = "/"+self.kwargs['feeds']
        except KeyError:
            items = feed.keys()

        try:
            if self.kwargs['mode'] == "index" or self.kwargs['mode'] == "":
                if header == "Обновления":
                    items = list(feedUpdate.objects.filter(title__in=feed.keys())[:items_limit])
                else:
                    items = list(feedUpdate.objects.filter(title__in=self.kwargs['feeds'].split("+"))[:items_limit])
            elif self.kwargs['mode'] == "force":
                items = feedUpdate.multilist(items)
                items = sorted(items, key=lambda feedUpdate: str(feedUpdate.datetime), reverse=True)
            else:
                items = []
        except KeyError:
            if header == "Обновления":
                items = list(feedUpdate.objects.filter(title__in=feed.keys())[:items_limit])
            else:
                items = list(feedUpdate.objects.filter(title__in=self.kwargs['feeds'].split("+"))[:items_limit])

        try:
            if self.kwargs['mode'] == "force":
                header += ": Forced"
        except KeyError:
            pass

        return {
            'title': header,
            'items': items,
            'multibook': multibook,
        }
