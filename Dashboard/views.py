from django.views.generic import ListView
from .models import PlanetaKino
from datetime import datetime, time


class DashboardView(ListView):
    template_name = "Dashboard/main.html"
    context_object_name = "fromView"

    def get_queryset(self):
        header_night = "Доброй ночи"
        header_morning = "Доброе утро"
        header_day = "Привет"
        header_evening = "Доброго вечера"

        now = datetime.now().time()
        if now < time(6):
            title_daypart = header_night
        elif now < time(12):
            title_daypart = header_morning
        elif now < time(18):
            title_daypart = header_day
        else:
            title_daypart = header_evening

        movies = PlanetaKino.objects.filter(inTheater=True)

        return {
            'title_daypart': title_daypart,
            'movies': movies,
        }
