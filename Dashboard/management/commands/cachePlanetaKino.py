from django.core.management.base import BaseCommand, CommandError
from Dashboard.models import PlanetaKino
import time

class Command(BaseCommand):
    help = 'cache PlanetaKino items to DB'

    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true')

    def handle(self, *args, **options):
        # execution preparation
        if options['log']:
            total_start = time.time()
            total_items = 0
            print("┣ starting")

        PlanetaKino.objects.all().delete()

        # parsing
        movies = PlanetaKino.list()
        for each in movies:
            each.save()

            if options['log']:
                total_items += 1

        if options['log']:
            total_end = time.time()
            total_time = round(total_end - total_start, 2)
            print("└──── added " + str(total_items) + " in " + str(total_time) + "s")
