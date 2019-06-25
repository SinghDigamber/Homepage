from django.core.management.base import BaseCommand, CommandError
from calenda.models import calendar, event
import time
from tqdm import tqdm

class Command(BaseCommand):
    help = 'updates caches in DB'

    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true')
        parser.add_argument('--logEach', action='store_true')
        parser.add_argument('--logBar', action='store_true')

        parser.add_argument('--parseCalendars', action='store_true')
        parser.add_argument('--parseEvents', action='store_true')

    def handle(self, *args, **options):
        # execution preparation
        if options['log']:
            total_start = time.time()
            total_items = 0
            print("┣ starting")

        # parsing feedUpdate/feeds from feeds.py
        if options['parseCalendars']:
            # cycle preparation
            if options['logEach']:
                cycle_start = time.time()
                cycle_items = 0

            # removing all old feeds to avoid conflicts
            calendar.objects.all().delete()

            parse_calendars = list(calendar.calendars_from_file())
            if options['logBar']:
                parse_calendars = tqdm(parse_calendars)
            # parsing from file to database
            for each in parse_calendars:
                each.save()
                if options['log']:
                    total_items += 1
                if options['logEach']:
                    cycle_items += 1

            # cycle result printing
            if options['logEach']:
                cycle_end = time.time()
                cycle_time = round(cycle_end - cycle_start, 2)
                print("┣ added " + str(cycle_items) + " feeds in " + str(cycle_time) + "s")

        # caching feedUpdates for feeds stored in DB
        if options['parseEvents']:
            event.objects.all().delete()

            parse_calendars = list(calendar.objects.all())
            if options['logBar']:
                parse_calendars = tqdm(parse_calendars)

            # parsing from file to database
            for current_calendar in parse_calendars:
                # cycle preparation
                if options['logEach']:
                    cycle_start = time.time()
                    cycle_items = 0

                for each in current_calendar.parse():
                    # TODO: check for duplicates
                    each.save()
                    if options['log']:
                        total_items += 1
                    if options['logEach']:
                        cycle_items += 1

                if options['logEach']:
                    cycle_end = time.time()
                    cycle_time = round(cycle_end - cycle_start, 2)
                    print("┣ added " + current_calendar.title + " x" + str(cycle_items) + " in " + str(cycle_time) + "s")

        if options['log']:
            total_end = time.time()
            total_time = round(total_end - total_start, 2)
            print("└──── added " + str(total_items) + " in " + str(total_time) + "s")
