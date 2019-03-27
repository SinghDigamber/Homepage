from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino
# from datetime import datetime

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
            newItems = 0

        # parsing feeds from feeds.py
        if options['feeds']:
            # removing old ones if present
            feed.objects.all().delete()
            # saving to database
            for each in feed.feeds_from_file():
                each.save()
                if options['log']:
                    newItems += 1

        # feedUpdate caching mode choosing
        if options['all'] or options['inIndex']:
            feeds_to_parse = []
            if options['all']:
                feeds_to_parse = list(feed.objects.all())
            elif options['inIndex']:
                feeds_to_parse = list(feed.feeds_by_emoji())

            feedUpdate_results = []
            for each in feeds_to_parse:
                for feedUpdate_item in each.parse():
                    feedUpdate_results.append(feedUpdate_item)

            for each in feedUpdate_results:
                if not feedUpdate.objects.filter(
                    # name=item.name,
                    href=each.href,
                    # datetime=item.datetime,
                    # title=item.title
                ).exists():
                    # item.datetime = datetime.now()
                    # print(item)
                    each.save()
                    if options['log']:
                        newItems += 1

        if options['PlanetaKino']:
            PlanetaKino.objects.all().delete()
            movies = PlanetaKino.list()
            for each in movies:
                if not PlanetaKino.objects.filter(
                    href=each.href,
                ).exists():
                    each.save()
                    if options['log']:
                        newItems += 1

        if options['log']:
            print("└──── added " + str(newItems))
