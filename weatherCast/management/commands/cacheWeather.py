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
        keyValue.objects.filter(key='weatherNowProb').delete()
        keyValue.objects.filter(key='weatherNowIcon').delete()

        title_weather = weatherCast.parse_json_weather_now_summary_compiled(
            weatherCast.download_weather_forecast())

        summary = keyValue(key='weatherNowSum', value=title_weather['summary'])
        temp = keyValue(key='weatherNowTemp', value=title_weather['temp'])
        precipProbability = keyValue(key='weatherNowProb', value=title_weather['precipProbability'])
        icon = keyValue(key='weatherNowIcon', value=title_weather['icon'])

        summary.save()
        temp.save()
        precipProbability.save()
        icon.save()
