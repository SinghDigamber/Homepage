from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino
import time

class Command(BaseCommand):
    help = 'Caches new information'

    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true')
        parser.add_argument('--logEach', action='store_true')

        parser.add_argument('--parseFeeds', action='store_true')
        parser.add_argument('--parseAll', action='store_true')
        parser.add_argument('--parseIndex', action='store_true')

        parser.add_argument('--parsePlanetaKino', action='store_true')

    def handle(self, *args, **options):
        # execution preparation
        if options['log']:
            total_start = time.time()
            total_items = 0
            print("┣ starting")
        lens = [0]

        # parsing feedUpdate/feeds from feeds.py
        if options['parseFeeds']:
            # cycle preparation
            if options['logEach']:
                cycle_start = time.time()
                cycle_items = 0

            # removing all old feeds to avoid conflicts
            feed.objects.all().delete()

            # parsing from file to database
            for each in feed.feeds_from_file():
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
        if options['parseAll'] or options['parseIndex']:
            # prepare list of feeds to parse
            parse_feeds = []
            if options['parseAll']:
                parse_feeds = list(feed.objects.all())
            elif options['parseIndex']:
                parse_feeds = list(feed.feeds_by_emoji())

            # parsing
            for current_feed in parse_feeds:
                # cycle preparation
                if options['logEach']:
                    cycle_start = time.time()
                    cycle_items = 0

                for feedUpdate_parsed_item in current_feed.parse():
                    if not feedUpdate.objects.filter(
                        # name=feedUpdate_parsed_item.name,
                        href=feedUpdate_parsed_item.href,
                        # datetime=feedUpdate_parsed_item.datetime,
                        # title=feedUpdate_parsed_item.title
                    ).exists():
                        # feedUpdate_parsed_item.datetime = datetime.now()
                        # print(feedUpdate_parsed_item)
                        feedUpdate_parsed_item.save()

                        if options['log']:
                            total_items += 1
                        if options['logEach']:
                            cycle_items += 1

                if options['logEach']:
                    cycle_end = time.time()
                    cycle_time = round(cycle_end - cycle_start, 2)
                    print("┣ added " + current_feed.title + " x" + str(cycle_items) + " in " + str(cycle_time) + "s")

        if options['parsePlanetaKino']:
            # cycle preparation
            if options['logEach']:
                cycle_start = time.time()
                cycle_items = 0

            # parsing
            PlanetaKino.objects.all().delete()
            movies = PlanetaKino.list()
            for each in movies:
                if not PlanetaKino.objects.filter(
                    href=each.href,
                ).exists():
                    each.save()
                    if options['log']:
                        total_items += 1
                    if options['logEach']:
                        cycle_items += 1
            if options['logEach']:
                cycle_end = time.time()
                cycle_time = round(cycle_end - cycle_start, 2)
                print("┣ added " + str(cycle_items) + " PlanetaKino items" + " in " + str(cycle_time) + "s")

        if options['log']:
            total_end = time.time()
            total_time = round(total_end - total_start, 2)
            print("└──── added " + str(total_items) + " in " + str(total_time) + "s")
