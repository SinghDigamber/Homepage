from django.core.management.base import BaseCommand
from weatherCast.models import weatherCast
from Dashboard.models import keyValue
import time

class Command(BaseCommand):
    help = 'cache weather forecast'

    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true')

    def handle(self, *args, **options):

        title_weather = weatherCast.parse_json_weather_now_summary_compiled(
            weatherCast.download_weather_forecast())

        for each in title_weather.keys():
            if len(keyValue.objects.filter(key=each)) > 0:
                summary = keyValue.objects.filter(key=each)[0]
                summary.value = title_weather[each]
                summary.save()
            else:
                summary = keyValue(key=each, value=title_weather[each])
                summary.save()
