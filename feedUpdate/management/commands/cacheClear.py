from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino

class Command(BaseCommand):
    help = 'removes all cache from DB'

    def handle(self, *args, **options):
        feedUpdate.objects.all().delete()
        feed.objects.all().delete()
        PlanetaKino.objects.all().delete()
