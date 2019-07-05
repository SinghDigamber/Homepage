from django.core.management.base import BaseCommand
from weatherCast.models import weatherCast
from Dashboard.models import keyValue
import time

class Command(BaseCommand):
    help = 'cache weather forecast'

    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true')

    def handle(self, *args, **options):
        keyValue.objects.filter(key='weatherNowSum').delete()
        keyValue.objects.filter(key='weatherNowTemp').delete()

        title_weather = weatherCast.parse_json_weather_now_summary_compiled(
            weatherCast.download_weather_forecast())

        summary = keyValue(key='weatherNowSum', value=title_weather['summary'])
        temp = keyValue(key='weatherNowTemp', value=title_weather['temp'])

        summary.save()
        temp.save()
