from django.shortcuts import render
from .models import chapters
from django.views.generic import ListView

# Create your views here.
class IndexView(ListView):
    model = chapters
    template_name = "bookUpdates/_index.html"
    context_object_name = "list"

    def get_queryset(self):
        items = []
        items.append('Скульптор')
        items.append('Система')

        items = chapters.multilist(items)
        items = sorted(items, key=lambda chapters: chapters.datetime, reverse=True)

        return {'title': 'Обновления', 'title_full': 'Обновления', 'chapters': items, 'multibook': True}


class IndexSystemView(ListView):
    model = chapters
    template_name = "bookUpdates/_index.html"
    context_object_name = "list"

    def get_queryset(self):
        book = 'Система'
        return {
            'title': book,
            'title_full': chapters.books[book]['title_full'],
            'chapters': chapters.list(book),
            'multibook': False}



class IndexSculptorView(ListView):
    model = chapters
    template_name = "bookUpdates/_index.html"
    context_object_name = "list"

    def get_queryset(self):
        book = 'Скульптор'
        return {
            'title': book,
            'title_full': chapters.books[book]['title_full'],
            'chapters': chapters.list(book),
            'multibook': False}