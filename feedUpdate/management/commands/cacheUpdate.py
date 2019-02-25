from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed, feeds
from datetime import datetime

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

    def handle(self, *args, **options):
        for each in feeds:
            each.save()

        print("┣ starting")
        newItems = 0

        if options['all']:
            items = list(feed.keysAll())
        if options['index']:
            items = list(feed.keys())
        else:
            items = list(feed.keysAll())

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

        print("└──── added " + str(newItems))
