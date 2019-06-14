from django.views.generic import ListView
from .models import PlanetaKino
from datetime import datetime, time
from weatherCast.models import weatherCast
from feedUpdate.models import feedUpdate, feed


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

        title_weather = weatherCast.parse_json_weather_now_summary_compiled(
            weatherCast.download_weather_forecast())

        movies = PlanetaKino.objects.filter(inTheater=True)

        feedUpdate_size_limit = 42
        feed_title_list = []
        for each in feed.feeds_by_emoji():
            feed_title_list.append(each.title)
        feedUpdate_list = list(feedUpdate.objects.filter(title__in=feed_title_list)[:feedUpdate_size_limit])

        return {
            'title_daypart': title_daypart,
            'title_weather': title_weather,
            'movies': movies,
            'feedUpdate_list': feedUpdate_list,
        }
