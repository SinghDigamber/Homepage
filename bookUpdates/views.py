from django.shortcuts import render
from .models import bookUpdate
from django.views.generic import ListView
import socket
from django.shortcuts import redirect


class bookUpdateForceIndexView(ListView):
    model = bookUpdate
    template_name = "bookUpdates/_index.html"
    context_object_name = "list"

    def get_queryset(self):
        header = "Forced!"
        multibook = True

        try:
            if self.kwargs['books'] != "":
                header = self.kwargs['books']

                items = self.kwargs['books']
                items = items.split("+")
                if len(items) == 1:
                    multibook = False
        except KeyError:
            items = bookUpdate.books.keys()

        items = bookUpdate.multilist(items)
        items = sorted(items, key=lambda bookUpdate: str(bookUpdate.datetime), reverse=True)

        return {
            'title': header,
            'chapters': items,
            'multibook': multibook
        }


class bookUpdateIndexView(ListView):
    model = bookUpdate
    template_name = "bookUpdates/_index.html"
    context_object_name = "list"

    def get_queryset(self):
        header = "Обновления"
        multibook = True

        try:
            if self.kwargs['books'] != "":
                header = self.kwargs['books']

                items = self.kwargs['books']
                items = items.split("+")
                if len(items) == 1:
                    multibook = False
                items = list(bookUpdate.objects.filter(title__in=items))[:20]
        except KeyError:
            items = list(bookUpdate.objects.all())[:20]

        return {
            'title': header,
            'chapters': items,
            'multibook': multibook
        }

class bookUpdateCacheView(ListView):
    model = bookUpdate
    template_name = "bookUpdates/_index.html"

    def get_queryset(self):
        bookUpdate.cache()

        return {
            'title': "Cache updated",
            'chapters': list(bookUpdate.objects.all())[:20],
            'multibook': True
        }
