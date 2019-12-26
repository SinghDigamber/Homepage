from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from Dashboard.models import PlanetaKino
import time
from datetime import datetime
from tqdm import tqdm
from random import shuffle
import requests
from concurrent.futures import ThreadPoolExecutor

class Command(BaseCommand):
    help = 'updates caches in DB'

    def add_arguments(self, parser):
        # parsing mode
        parser.add_argument('--parseFeeds', action='store_true')
        parser.add_argument('--parseUpdates', action='store_true')
        
        # parsing modifiers
        parser.add_argument('--shuffle', action='store_true')
        parser.add_argument('--useProxy', action='store_true')
        parser.add_argument('--printEmpty', action='store_true')

        # logging options
        parser.add_argument('--log', action='store_true')
        parser.add_argument('--logEach', action='store_true')
        parser.add_argument('--logBar', action='store_true')

    def print_feed(amount, time, title):
        print(f"┣ added {title} x{str(amount)} in {str(time)}s")

    def print_total(amount, time):
        print(f"└──── added {str(amount)} in {str(time)}s")

    def process_feed(current_feed):
        # cycle preparation
        cycle_time = time.time()
        cycle_items = 0
        cycle_items_total = 0

        # PARSING HERE
        feedUpdate_list = current_feed.parse()
        print("1 parsed: ", 1000*(time.time() - cycle_time, 2))
        feedUpdate_list = reversed(feedUpdate_list)
        print("2 reversed: ", 1000*(time.time() - cycle_time, 2))

        # checking if feed is new: new feeds use real datetime
        new_feed = True if len(feedUpdate.objects.filter(title=current_feed.title)) == 0 else False
        print("3 checked: ", 1000*(time.time() - cycle_time, 2))

        for each in feedUpdate_list:
            # checking if href is cached
            cached = feedUpdate.objects.filter(href=each.href).exists()
            
            cycle_items_total += 1
            if not cached:
                if new_feed:
                    each.datetime = datetime.now()
                
                each.save()
                cycle_items += 1
        print("4 saved: ", 1000*(time.time() - cycle_time, 2))

        cycle_time = time.time() - cycle_time
        cycle_time = round(cycle_time, 2)

        cycle_result = {
            'title': current_feed.title, 
            'time': cycle_time, 
            'amount': cycle_items,
            'amount_total': cycle_items_total
        }
        return(cycle_result)

    def handle(self, *args, **options):
        try:  # KeyboardInterrupt for Ctrl+C stops
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
                    cycle_time = time.time()
                    cycle_time = round(cycle_time - cycle_start, 2)
                    Command.print_feed(
                        title="feeds",
                        amount=total_items, 
                        time=cycle_time
                    )

            # caching feedUpdates for feeds stored in DB
            if options['parseUpdates']:
                proxy = False
                if options["useProxy"]:
                    proxy = requests.get('http://pubproxy.com/api/proxy?https=true&user_agent=true&referer=true').json()['data'][0]["ipPort"]
                    
                # prepare list of feeds to parse
                parse_feeds = []
                parse_feeds = list(feed.objects.all())

                if options['shuffle']:
                    shuffle(parse_feeds)

                with ThreadPoolExecutor() as executor:
                    executor = executor.map(Command.process_feed, parse_feeds)
                    if options['logBar']:
                        executor = tqdm(executor, total=len(parse_feeds))

                    for result in executor:
                        if options['logEach'] or (options["printEmpty"] and result['amount_total'] == 0):
                            Command.print_feed(
                                title=result['title'], 
                                amount=result['amount'], 
                                time=result['time']
                            )
                        
                        if options['log']:
                            total_items += result['amount']
                        break

            if options['log']:
                total_time = time.time()
                total_time = round(total_time - total_start, 2)
                Command.print_total(
                    amount=total_items, 
                    time=total_time
                )
                
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt: execution aborted')