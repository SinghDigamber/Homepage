from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino
import time
from datetime import datetime
from tqdm import tqdm
from random import shuffle
import requests

class Command(BaseCommand):
    help = 'updates caches in DB'

    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true')
        parser.add_argument('--logEach', action='store_true')
        parser.add_argument('--logBar', action='store_true')

        parser.add_argument('--shuffle', action='store_true')
        parser.add_argument('--useProxy', action='store_true')
        parser.add_argument('--printEmpty', action='store_true')

        parser.add_argument('--parseFeeds', action='store_true')
        parser.add_argument('--parseAll', action='store_true')
        parser.add_argument('--parseIndex', action='store_true')
        parser.add_argument('--parseNow', action='store_true')

    def handle(self, *args, **options):
        # execution preparation
        if options['log']:
            total_start = time.time()
            total_items = 0
            print("┣ starting")

        # parsing feedUpdate/feeds from feeds.py
        if options['parseFeeds']:
            # cycle preparation
            if options['logEach']:
                cycle_start = time.time()
                cycle_items = 0

            # removing all old feeds to avoid conflicts
            feed.objects.all().delete()

            # parsing from file to database
            parse_feeds = feed.feeds_from_file()
            if options['logBar']:
                parse_feeds = tqdm(parse_feeds)
            for each in parse_feeds:
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
            proxy = False
            if options["useProxy"]:
                proxy = requests.get('http://pubproxy.com/api/proxy?https=true&user_agent=true&referer=true').json()['data'][0]["ipPort"]
                
            # prepare list of feeds to parse
            parse_feeds = []
            if options['parseAll']:
                parse_feeds = list(feed.objects.all())
            elif options['parseIndex']:
                parse_feeds = list(feed.feeds_by_emoji())

            if options['shuffle']:
                shuffle(parse_feeds)

            # parsing
            if options['logBar']:
                parse_feeds = tqdm(parse_feeds)
            for current_feed in parse_feeds:
                # cycle preparation
                if options['logEach']:
                    cycle_start = time.time()
                    cycle_items = 0
                
                feedUpdate_list = current_feed.parse(proxy)

                if options["printEmpty"]:
                    if len(feedUpdate_list) == 0 and current_feed.filter == None:
                        print(current_feed.href)
                
                if options['parseNow']:
                    feedUpdate_list = reversed(feedUpdate_list)

                for each in feedUpdate_list:
                    # checking if href is cached
                    cached = feedUpdate.objects.filter(href=each.href).exists()

                    if not cached:
                        if options['parseNow']:
                            each.datetime = datetime.now()
                        each.save()

                        if options['log']:
                            total_items += 1
                        if options['logEach']:
                            cycle_items += 1

                if options['logEach']:
                    cycle_end = time.time()
                    cycle_time = round(cycle_end - cycle_start, 2)
                    print("┣ added " + current_feed.title + " x" + str(cycle_items) + " in " + str(cycle_time) + "s")

        if options['log']:
            total_end = time.time()
            total_time = round(total_end - total_start, 2)
            print("└──── added " + str(total_items) + " in " + str(total_time) + "s")
