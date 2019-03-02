from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino
# from datetime import datetime

class Command(BaseCommand):
    help = 'Caches new information'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            help='run full caching: no sense is usage as it is used by default',
        )

        parser.add_argument(
            '--inIndex',
            action='store_true',
            dest='index',
            help='run caching ONLY for items in INDEX',
        )

        parser.add_argument(
            '--PlanetaKino',
            action='store_true',
            dest='PlanetaKino',
            help='run caching ONLY for items from Dashboard.PlanetaKino',
        )

    def handle(self, *args, **options):

        print("┣ starting")
        newItems = 0

        # adding feeds to database for admin usage
        feed.objects.all().delete()
        for each in feed.all():
            each.save()

        if options['all']:
            items = list(feed.keysAll())
        elif options['index']:
            items = list(feed.keys())
        else:
            items = []

        items = feedUpdate.multilist(items)

        for item in items:
            if not feedUpdate.objects.filter(
                # name=item.name,
                href=item.href,
                # datetime=item.datetime,
                # title=item.title
            ).exists():
                # item.datetime = datetime.now()
                # print(item)
                item.save()
                newItems += 1

        if options['PlanetaKino']:
            movies = PlanetaKino.list()
            for each in movies:
                if not PlanetaKino.objects.filter(
                    href=each.href,
                ).exists():
                    each.save()
                    newItems += 1


        print("└──── added " + str(newItems))
