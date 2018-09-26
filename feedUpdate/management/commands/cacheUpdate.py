from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from datetime import datetime

class Command(BaseCommand):
    help = 'Caches new information'

    def handle(self, *args, **options):
        print("┣ starting")
        newItems = 0

        items = list(feed.keysAll())
        items = feedUpdate.multilist(items)

        for item in items:
            if not feedUpdate.objects.filter(
                    # name=item.name,
                    href=item.href,
                    # datetime=item.datetime,
                    # title=item.title
            ).exists():
                # print(item)
                item.save()
                newItems += 1

        print("└──── added " + str(newItems))
