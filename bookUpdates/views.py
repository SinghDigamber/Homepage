from django.shortcuts import render
from .models import chapters
from django.views.generic import ListView

# Create your views here.
class BookIndexView(ListView):
    model = chapters
    template_name = "bookUpdates/_index.html"
    context_object_name = "list"

    def get_queryset(self):
        try:
            if self.kwargs['books'] != "":
                items = self.kwargs['books']
                items = items.split("+")
            else:
                items = chapters.books.keys()
        except KeyError:
            items = chapters.books.keys()

        items = chapters.multilist(items)
        items = sorted(items, key=lambda chapters: str(chapters.datetime), reverse=True)

        return {'title': 'Обновления', 'title_full': 'Обновления', 'chapters': items, 'multibook': True}
