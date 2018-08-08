from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate

class Command(BaseCommand):
    help = 'removes all information from database'

    def handle(self, *args, **options):
        feedUpdate.objects.all().delete()