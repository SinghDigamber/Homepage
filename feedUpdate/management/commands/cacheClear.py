from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino

class Command(BaseCommand):
    help = 'cleares cache in DB'

    def handle(self, *args, **options):
        feedUpdate.objects.all().delete()
        PlanetaKino.objects.all().delete()
