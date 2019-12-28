from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
# from collections import OrderedDict
import urllib.request, feedparser
from datetime import datetime, timedelta
# from pytz import timezone
from django.utils.timezone import localtime
# from datetime import timezone
import json
import dateutil.parser as datetimeparser
from dateutil.tz import gettz
from random import randint
from Dashboard.models import keyValue
import os


class feed(models.Model):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=42)
    title_full = models.CharField(max_length=140, null=True)
    href = models.CharField(max_length=420)
    href_title = models.CharField(max_length=420, null=True)
    emojis = models.CharField(max_length=7, null=True)  # usage as tags
    filter = models.CharField(max_length=140, null=True)
    delay = models.IntegerField(null=True)

    # to string
    def __str__(self):
        result = "["+self.title+"]"
        if self.title_full is not None:
            result += ": "+self.title_full
        if self.emojis is not None:
            result += " e: "+self.emojis
        if self.filter is not None:
            result += " f: "+self.filter
        if self.delay is not None:
            result += " d: "+str(self.delay)
        if self.href is not None:
            result += " href: "+self.href
        if self.href_title is not None:
            result += " href_title: "+self.href_title
        return result

    # return <feed> by feed.title
    @staticmethod
    def find(searched_title):
        for each in feed.objects.all():
            if each.title == searched_title:
                return each

    # return List<feed> by emoji
    @staticmethod
    def feeds_by_emoji(emoji_filter='💎'):
        if len(emoji_filter) == 1:
            result = []
            for each in feed.objects.all():
                if each.emojis != None and each.emojis.find(emoji_filter) != -1:
                    result.append(each)
            return result
        else:
            error = "len(emoji_filter) is not 1"
            print(error)
            return [error]

    # return List<feed> from feedUpdate/feeds.py
    def feeds_from_file():
        from .feeds import feeds
        return feeds

    def UserAgent_random():
        f=open(os.path.join("static", "feedUpdate", 'user-agents.txt'))

        line_number = keyValue.objects.filter(key='UserAgentLen')[0]
        line_number = int(line_number.value)
        line_number = randint(1, line_number)
        useragent = f.read().split('\n')[line_number-1]
        f.close()
        return useragent

    # return List<feedUpdate> parsed from source by <feed> (self)
    def parse(self, proxy=False):
        result = []

        # avoiding blocks
        headers = {
            'user-agent': feed.UserAgent_random().lstrip(),
            'referer': 'https://www.google.com/search?newwindow=1&q='+self.href
        }
        if proxy != False:
            proxyDict = {
                "http": "http://" + proxy, 
                "https": "https://" + proxy,
            }
        else:
            proxyDict = {}

        # custom ранобэ.рф API import
        if self.href.find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            request = f"https://xn--80ac9aeh6f.xn--p1ai/api/v2/books/{ self.href[31:-1] }/chapters"
            request = requests.get(request).json()  # (request, headers=headers, proxies=proxyDict)

            for each in request['items']:
                # ignoring payed chapters
                if each['availabilityStatus'] == 'free':
                    result.append(feedUpdate(
                        name=each["title"],
                        href="http://xn--80ac9aeh6f.xn--p1ai"+each["url"],
                        datetime=datetime.strptime(each["publishTime"], '%Y-%m-%d %H:%M:%S'),
                        title=self.title))

        # custom instagram import
        if self.href.find('https://www.instagram.com/') != -1:
            if not randint(0, 100) == 0:
                return []
            try:
                request = requests.get(self.href, headers=headers, proxies=proxyDict)
                request = BeautifulSoup(request.text, "html.parser")

                for each in request.find_all('script'):
                    data_start = 'window._sharedData = '
                    if each.text.find(data_start) != -1:
                        # preparing JSON
                        data_start = each.text.find(data_start)+len(data_start)
                        data = str(each.text)[data_start:-1]  # -1 is for removing ; in the end
                        data = json.loads(data)
                        data = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']

                        # parsing data from JSON
                        for each in data:
                            each = each['node']

                            # avoiding errors caused by empty titles
                            try:
                                result_name = each['edge_media_to_caption']['edges'][0]['node']['text']
                            except IndexError:
                                result_name = 'no title'

                            result_href = "http://instragram.com/p/"+each['shortcode']

                            result_datetime = each['taken_at_timestamp']
                            result_datetime = datetime.fromtimestamp(result_datetime)

                            result.append(feedUpdate(
                                href=result_href,
                                datetime=result_datetime,
                                name=result_name,
                                title=self.title))
            except (KeyError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as err:
                return []

        # custom RSS YouTube converter (link to feed has to be converted manually)
        elif self.href.find('https://www.youtube.com/channel/') != -1:
            self.href_title = self.href[:]
            self.href = "https://www.youtube.com/feeds/videos.xml?channel_id="+self.href[32:-len('/videos')]
            result = feed.parse(self)

        # custom RSS readmanga converter (link to feed has to be converted manually to simplify feed object creation)
        elif self.href.find('http://readmanga.me/') != -1 and self.href.find('readmanga.me/rss/manga') == -1 and self.href_title == None:
            self.href = "feed://readmanga.me/rss/manga?name="+self.href[len('http://readmanga.me/'):]
            result = feed.parse(self)

        # custom RSS mintmanga converter (link to feed has to be converted manually to simplify feed object creation)
        elif self.href.find('http://mintmanga.com/') != -1 and self.href.find('mintmanga.com/rss/manga') == -1 and self.href_title == None:
            self.href = "feed://mintmanga.com/rss/manga?name="+self.href[len('http://mintmanga.com/'):]
            result = feed.parse(self)

        # custom RSS deviantart converter (link to feed has to be converted manually to simplify feed object creation)
        elif self.href.find('https://www.deviantart.com/') != -1:
            self.href_title = self.href[:]
            self.href = self.href[len('https://www.deviantart.com/'):-len('/gallery/')]
            self.href = "http://backend.deviantart.com/rss.xml?q=gallery%3A"+self.href
            result = feed.parse(self)

        # custom fantasy-worlds.org loader
        elif self.href.find('https://fantasy-worlds.org/series/') != -1:
            request = requests.get(self.href, headers=headers, proxies=proxyDict)
            strainer = SoupStrainer('div', attrs={'class': 'rightBlock'})
            request = BeautifulSoup(request.text, "html.parser", parse_only=strainer)

            for book in request.find('ul').find('li').find('ul').find('li').find('ul').find_all('li'):
                #print(book)

                result_name = book.text.find(' // ')
                result_name = self.title +" "+ book.text[:result_name]

                result_href = book.find('a')['href']

                result_datetime = datetime.now()

                result.append(feedUpdate(
                    name=result_name[:140],
                    href=result_href,
                    datetime=result_datetime,
                    title=self.title))

        # custom patreon.com loader
        #elif self.href.find('https://www.patreon.com/') != -1:
            #request = requests.get(self.href, headers=headers, proxies=proxyDict)
            #request = BeautifulSoup(request.text, "html.parser")

            #print(request.find('Object.assign(window.patreon.bootstrap, {')

            # cloudflare block,

            #pass

        # custom pikabu import
        elif self.href.find('pikabu.ru/@') != -1:
            try:
                request = requests.get(self.href, headers=headers, proxies=proxyDict)
                strainer = SoupStrainer('div', attrs={'class': 'stories-feed__container'})
                request = BeautifulSoup(request.text, "html.parser", parse_only=strainer)

                for article in request.find_all('article'):
                    try:
                        result_name = article.find('h2', {'class': "story__title"}).find('a').getText()

                        result_href = article.find('h2', {'class': "story__title"}).find('a')['href']

                        result_datetime = article.find('time')['datetime'][:-3]+"00"
                        result_datetime = datetime.strptime(result_datetime, '%Y-%m-%dT%H:%M:%S%z')

                        result.append(feedUpdate(
                            name=result_name[:140],
                            href=result_href,
                            datetime=result_datetime,
                            title=self.title))

                    except TypeError:
                        # advertisement, passing as no need to save it
                        pass
                    except AttributeError:
                        # advertisement, passing as no need to save it
                        pass
            except requests.exceptions.SSLError:
                # failed connection, hope it works from time to time
                return []
            except requests.exceptions.ConnectionError:
                return []

        # # custom vas3k pain parser
        # elif self.href.find('https://pain.vas3k.ru') != -1:
        #     request = requests.get(self.href, headers=headers, proxies=proxyDict)
        #     strainer = SoupStrainer('div', attrs={'id': 'pain-list'})
        #     request = BeautifulSoup(request.text, "html.parser", parse_only=strainer)

        #     for pain in request.find('div').find_all('div', attrs={'class': 'pain-item'}):
        #         #result_name = pain.find_all('div')[1].find('a').text
        #         #result_name += " > "
        #         result_name = pain.find_all('div')[2].find('p').text

        #         result_href = "https://pain.vas3k.ru" + pain.find_all('div')[1].find('a').get('href')

        #         # TODO: parse real datetime
        #         result_datetime = datetime.now()

        #         result.append(feedUpdate(
        #             name=result_name[:140],
        #             href=result_href,
        #             datetime=result_datetime,
        #             title=self.title))

        # custom fanserials parser
        elif self.href.find('http://fanserials.tv/') != -1 and self.filter is not None:
            request = requests.get(self.href, headers=headers, proxies=proxyDict)
            strainer = SoupStrainer('ul', attrs={'id': 'episode_list'})
            request = BeautifulSoup(request.text, "html.parser", parse_only=strainer)

            for item in request.find_all('li'):
                result_name = item.find('div', attrs={'class': 'field-description'}).find('a').text
                #print(result_name)

                result_href = ''
                for span in item.find('div').find('div', attrs={'class': 'serial-translate'}).find_all('span'):
                    # print(span)
                    if str(span.find('a')).find(self.filter) != -1:
                        result_href = 'http://fanserials.tv' + span.find('a').get('href')
                #print(result_href)

                # TODO: parse real datetime
                result_datetime = datetime.now()

                result.append(feedUpdate(
                    name=result_name[:140],
                    href=result_href,
                    datetime=result_datetime,
                    title=self.title))

        # default RSS import
        else:
            proxyDict = urllib.request.ProxyHandler(proxyDict)
            request = feedparser.parse(self.href, request_headers=headers, handlers=[proxyDict])

            for item in request["items"]:
                # NAME RESULT
                result_name = item["title_detail"]["value"]


                # HREF RESULT
                if self.title == "Expresso":
                    result_href = item["summary"]
                    result_href = result_href[result_href.find("https://expres.co/"):]
                    result_href = result_href[:result_href.find('"')]
                else:
                    result_href = item["links"][0]["href"]

                '''
                media_thumbnail = ""
                try:
                    media_thumbnail = item['media_thumbnail'][0]['url']
                    media_thumbnail = len(media_thumbnail)
                    if media_thumbnail >= 270:
                        print("too long: " + self.title)
                except KeyError:
                    media_thumbnail = self.title
                    # print("empty: " + media_thumbnail)
                '''

                # FILTERING: passing item cycle if filter does not match
                if self.filter is not None:
                    if result_name.find(self.filter) == -1 and result_href.find(self.filter) == -1:
                        continue


                # DATE RESULT: parsing dates
                # preparsing: choosing date string source
                if "published" in item:
                    result_datetime = item["published"]
                elif "updated" in item:
                    result_datetime = item["updated"]
                else:
                    # there was nothing to get as result_datetime
                    result_datetime = "Sun, 22 Oct 1995 00:00:00 +0200"

                tzinfos = {'PDT': gettz("America/Los_Angeles"), 'PST': gettz("America/Juneau")}
                # usage examples: {'EST': -1800, 'CET': +3600, "CST": gettz("America/Chicago")}
                result_datetime = datetimeparser.parse(result_datetime, tzinfos=tzinfos)

                # APPEND RESULT
                result.append(feedUpdate(
                    name=result_name[:140],
                    href=result_href,
                    datetime=result_datetime,
                    title=self.title))

        # universal postfixes
        for each in result:
            # DATETIME fixes
            # fix timezone unaware
            if each.datetime.tzinfo is not None and each.datetime.tzinfo.utcoffset(each.datetime) is not None:
                dateresult2 = localtime(each.datetime)
                each.datetime = datetime(dateresult2.year, dateresult2.month, dateresult2.day,
                     dateresult2.hour, dateresult2.minute, dateresult2.second)
            # add DELAY
            if type(self.delay) is not type(None):
                each.datetime += timedelta(hours=self.delay)

            # NAME fixes
            each.name = ' '.join(each.name.split())
            each.name = each.name[:140]  # SQLite does not support max-length
            # extra symbols
            if each.title == 'Shadman':
                each.name = each.name[:each.name.find('(')-1]
            elif each.title == 'Apple' and each.name[-len('Apple'):] == 'Apple':
                # - symbol can be a variety of different symbols
                each.name = each.name[:-len(' - Apple')]
            elif each.title == 'LastWeekTonight' and each.name.find(': Last Week Tonight with John Oliver (HBO)') != -1:
                each.name = each.name[:each.name.find(': Last Week Tonight with John Oliver (HBO)')]
            elif each.title == 'Expresso':
                each.name = each.name[len("YYYY-MM-DD "):]

        return result


class feedUpdate(models.Model):
    class Meta:
        ordering = ['-datetime']
    name = models.CharField(max_length=140)
    href = models.CharField(max_length=420)
    # href_thumbnail = models.CharField(max_length=140, null=True) # some links are waaay too long :(
    datetime = models.DateTimeField()
    title = models.CharField(max_length=42)

    def __str__(self):
        return "["+self.title+"]: "+self.name+" d: "+str(self.datetime)+" with link "+self.href