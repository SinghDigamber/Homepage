from django.shortcuts import render
from .models import chapters
from django.views.generic import ListView

# Create your views here.
class BookIndexView(ListView):
    model = chapters
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
        except KeyError:
            items = chapters.books.keys()

        items = chapters.multilist(items)
        items = sorted(items, key=lambda chapters: str(chapters.datetime), reverse=True)

        return {
            'title': header,
            'chapters': items,
            'multibook': multibook
        }
