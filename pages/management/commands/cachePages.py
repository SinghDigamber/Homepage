from django.core.management.base import BaseCommand, CommandError
from pages.models import page
import time
from tqdm import tqdm

class Command(BaseCommand):
    help = 'updates caches in DB'

    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true')
        parser.add_argument('--logBar', action='store_true')

        parser.add_argument('--parsePages', action='store_true')

    def handle(self, *args, **options):
        # execution preparation
        if options['log']:
            total_start = time.time()
            total_items = 0
            print("┣ starting")

        # parsing feedUpdate/feeds from feeds.py
        if options['parsePages']:
            # removing all old feeds to avoid conflicts
            page.objects.all().delete()

            # parsing from file to database
            page_list = page.parse()

            if options['logBar']:
                page_list = tqdm(page_list)
            for each in page_list:
                each.save()
                if options['log']:
                    total_items += 1

        if options['log']:
            total_end = time.time()
            total_time = round(total_end - total_start, 2)
            print("└──── added " + str(total_items) + " in " + str(total_time) + "s")
