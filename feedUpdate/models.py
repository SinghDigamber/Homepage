from django.db import models
# from bs4 import BeautifulSoup, SoupStrainer
import requests
# from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
from pytz import timezone
from django.utils.timezone import localtime
from datetime import timezone
# Create your models here.

# TODO: move project to actual database


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
            result += " href: "+self.href_title
        return result

    # find a feed by feed.title
    @staticmethod
    def find(the_title_we_search):
        # feed.objects.all().values(title=the_title_we_search)
        for each in feed.objects.all():
            if each.title == the_title_we_search:
                return each

    # return feeds which contain emoji X
    @staticmethod
    def feeds_by_emoji(emoji_filter='💎'):
        if len(emoji_filter) == 1:
            result = []
            for each in feed.objects.all():
                if each.emojis != None and each.emojis.find(emoji_filter) != -1:
                    result.append(each)
            return result
        else:
            return ["Wrong emoji_filter length"]

    def feeds_from_file():
        from .feeds import feeds
        return feeds

    def parse(self):
        print(type(self))
        result = []

        # custom ранобэ.рф API import
        # Warning! API can be closed
        if self.href.find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            request = "https://xn--80ac9aeh6f.xn--p1ai/v1/book/get/?bookAlias="+self.href[31:-1]
            request = requests.get(request).json()

            for each in request['result']['parts']:
                result.append(feedUpdate(
                    name=each["title"],
                    href="http://xn--80ac9aeh6f.xn--p1ai"+each["url"],
                    datetime=datetime.fromtimestamp(each["publishedAt"])+timedelta(hours=-1),
                    title=self.title))

        # custom RSS YouTube import (link to feed has to be converted manually)
        elif self.href.find('https://www.youtube.com/channel/') != -1:
            # -7 is /channel in the end of self.href
            self.href = "https://www.youtube.com/feeds/videos.xml?channel_id="+self.href[32:-7]
            result = feed.parse(self)

        # default RSS import
        else:
            rss = feedparser.parse(self.href)

            for item in rss["items"]:
                # FILTERING: passing item cycle if filter does not match
                if self.filter is not None:
                    if item["links"][0]["href"].find(self.filter) == -1 and item["title_detail"]["value"].find(self.filter) == -1:
                        continue

                # NAME RESULT: custom name fields
                if self.href.find("https://websta.me/rss/n/") != -1:
                    nameresult = item['summary']
                    nameresult = nameresult[:nameresult.find("<a href=")]
                else:
                    nameresult = item["title_detail"]["value"]

                # DATE RESULT: parsing dates
                # preparsing: choosing date string source
                if "published" in item:
                    datestring = item["published"]
                elif "updated" in item:
                    datestring = item["updated"]
                else:
                    datestring = "did not match date preparser"
                # print(item)

                # try-except-datetime-parsing
                try:
                    dateresult = datetime.strptime(datestring, '%a, %d %b %Y %H:%M:%S %z')
                except ValueError:
                    try:
                        dateresult = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                        if datestring[-3] == ':':  # YouTube / TheVerge
                            dateresult = datetime.strptime(datestring[:-3] + datestring[-2:], '%Y-%m-%dT%H:%M:%S%z')
                            # dateresult = datetime.strptime(datestring[-2:-3], '%Y-%m-%dT%H:%M:%S%z')
                        else:
                            try:  # except ValueError: # it is for webtooms import feeds['Gamer']
                                dateresult = datetime.strptime(datestring, '%A, %d %b %Y %H:%M:%S %Z')
                                # +timedelta(hours=3)
                            except ValueError:  # it is for pikabu Brahmanden import feeds['Brahmanden']
                                try:
                                    # .astimezone(timezone('UTC'))  # +timedelta(hours=3)
                                    dateresult = datetime.strptime(datestring, '%a, %d %b %Y %H:%M:%S %Z')
                                except ValueError: # idea-instructions.com
                                    try:
                                        dateresult = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S%z')
                                    except ValueError:
                                        dateresult = datetime.strptime(datestring[:-3], '%a, %d %b %Y %H:%M:%S ')
                                        dateresult = dateresult + timedelta(-9)

                # HREF RESULT: custom href fields
                if self.title == "Expresso":
                    counter = item["summary"].find("https://expres.co/")
                    if counter > 0:
                        hrefresult = item["summary"][counter:]
                        counter2 = hrefresult.find('"')
                        hrefresult = hrefresult[:counter2]
                    else:
                        continue
                else:
                    hrefresult = item["links"][0]["href"]

                # APPEND RESULT
                result.append(feedUpdate(
                    name=nameresult,
                    href=hrefresult,
                    datetime=dateresult,
                    title=self.title))

        # universal postfixes
        for each in result:
            # datetime fixes
            if each.datetime.tzinfo is not None and each.datetime.tzinfo.utcoffset(each.datetime) is not None:
                dateresult2 = localtime(each.datetime)
                each.datetime = datetime(dateresult2.year, dateresult2.month, dateresult2.day,
                     dateresult2.hour, dateresult2.minute, dateresult2.second)

            # DELAY updates datetime
            if type(self.delay) is not type(None):
                each.datetime = each.datetime + timedelta(hours=self.delay)

            # name fixes
            if each.title == 'Shadman':
                each.name = each.name[:each.name.find('(')-1]
            elif each.title == 'Apple':
                # 5 is len('Apple') while 8 — len(' - Apple') as - symbol can be a variety of separate symbols
                if each.name[len(each.name)-5:] == 'Apple':
                    each.name = each.name[:len(each.name)-8]
            elif each.title == 'LastWeekTonight':
                if each.name.find(': Last Week Tonight with John Oliver (HBO)') != -1:
                    each.name = each.name[:each.name.find(': Last Week Tonight with John Oliver (HBO)')]
            elif each.title == 'Expresso':
                # TODO: check what 11 is
                each.name = each.name[11:]

        return result


class feedUpdate(models.Model):
    class Meta:
        ordering = ['-datetime']
    name = models.CharField(max_length=140)
    href = models.CharField(max_length=210)
    datetime = models.DateTimeField()
    title = models.CharField(max_length=42)

    def __str__(self):
        return "["+self.title+"]: "+self.name+" d: "+str(self.datetime)+" with link "+self.href