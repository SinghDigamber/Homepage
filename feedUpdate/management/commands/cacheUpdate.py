from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino
import time

class Command(BaseCommand):
    help = 'Caches new information'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--log',
            action='store_true',
            dest='log',
            help='print logs',
        )

        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            help='run full feedUpdate caching',
        )

        parser.add_argument(
            '--inIndex',
            action='store_true',
            dest='inIndex',
            help='run caching ONLY for items in INDEX',
        )

        parser.add_argument(
            '--feeds',
            action='store_true',
            dest='feeds',
            help='run caching ONLY for items from feeds',
        )

        parser.add_argument(
            '--PlanetaKino',
            action='store_true',
            dest='PlanetaKino',
            help='run caching ONLY for items from Dashboard.PlanetaKino',
        )

    def handle(self, *args, **options):
        # preparing logs
        if options['log']:
            print("┣ starting")
            newItemsTotal = 0
            execution_start = time.time()

        # parsing feeds from feeds.py
        if options['feeds']:
            if options['log']:
                newItems = 0
                item_start = time.time()
            # removing old ones if present
            feed.objects.all().delete()
            # saving to database
            for each in feed.feeds_from_file():
                each.save()
                if options['log']:
                    newItems += 1
                    newItemsTotal += 1
            if options['log']:
                item_end = time.time()
                print("┣ added " + str(newItems) + " feeds in " + str(round(item_end - item_start, 2)) + "s")

        # feedUpdate caching mode choosing
        if options['all'] or options['inIndex']:
            if options['log']:
                newItems = 0
                item_start = time.time()
            feeds_to_parse = []
            if options['all']:
                feeds_to_parse = list(feed.objects.all())
            elif options['inIndex']:
                feeds_to_parse = list(feed.feeds_by_emoji())

            for feed_item_to_parse in feeds_to_parse:
                if options['log']:
                    newItems = 0
                    item_start = time.time()
                for feedUpdate_parsed_item in feed_item_to_parse.parse():
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
                            newItems += 1
                            newItemsTotal += 1
                if options['log']:
                    item_end = time.time()
                    print("┣ added " + feed_item_to_parse.title + " x" + str(newItems) + " in " + str(round(item_end - item_start, 2)) + "s")

        if options['PlanetaKino']:
            if options['log']:
                newItems = 0
            PlanetaKino.objects.all().delete()
            movies = PlanetaKino.list()
            for each in movies:
                if not PlanetaKino.objects.filter(
                    href=each.href,
                ).exists():
                    each.save()
                    if options['log']:
                        newItems += 1
                        newItemsTotal += 1
            if options['log']:
                item_end = time.time()
                print("┣ added " + str(newItems) + " PlanetaKino items" + " in " + str(round(item_end - item_start, 2)) + "s")

        if options['log']:
            execution_end = time.time()
            print("└──── added " + str(newItemsTotal) + " in " + str(round(execution_end - execution_start, 2)) + "s")

