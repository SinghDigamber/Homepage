from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate

class Command(BaseCommand):
    help = 'Caches new information'

    def handle(self, *args, **options):
        items = list(feedUpdate.feeds.keys())
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
