from django.db import models
# from bs4 import BeautifulSoup, SoupStrainer
import requests
# from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
from pytz import timezone
from django.utils.timezone import localtime
# Create your models here.

# TODO: move project to actual database



# emojis
# 🏮 - hide from fU/feeds
# 💎 - inIndex=True
# 🗃️ - inIndex=False


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

    def __str__(self):
        result = "["+self.title+"]"
        if self.title_full is not None:
            result += ": "+self.title_full
        if self.emojis is not None:
            result += " e: "+self.emojis
        if self.filter is not None:
            result += " f: "+self.filter
        if self.delay is not None:
            result += " d: "+self.delay
        if self.href is not None:
            result += " href: "+self.href
        if self.href_title is not None:
            result += " href: "+self.href_title
        return result

    def find(title):
        for each in feed.all():
            if each.title == title:
                return each

    def keys():
        result = []
        for each in feed.all():
            if each.emojis != None and each.emojis.find('💎') != -1:
                result.append(each.title)
        return result

    def keysAll():
        result = []
        for each in feed.all():
            result.append(each.title)
        return result

    def all():
        from .feeds import feeds
        return feeds


class feedUpdate(models.Model):
    class Meta:
        ordering = ['-datetime']
    name = models.CharField(max_length=140)
    href = models.CharField(max_length=210)
    datetime = models.DateTimeField()
    title = models.CharField(max_length=42)

    def __str__(self):
        return "["+self.title+"]: "+self.name+" d: "+str(self.datetime)+" with link "+self.href

    def multilist(items):
        # TODO: warn if wrong filters were used
        result = []
        for item in items:
            try:
                result.extend(feedUpdate.list(item, feed.find(item).href, feed.find(item).filter))
            except KeyError:
                result.append(feedUpdate(
                    name="not found in feeds",
                    href="#",
                    datetime=datetime.now()+timedelta(hours=-3),
                    title=item))
                print("item: not found in feeds")

        return result

    def list(feedName, href, filter):
        result = []

        # custom ранобэ.рф API import
        # TODO: Warning! API can be closed
        if href.find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            request = "https://xn--80ac9aeh6f.xn--p1ai/v1/book/get/?bookAlias="+href[31:-1]
            request = requests.get(request).json()  # 0.4 seconds

            for each in request['result']['parts']:
                result.append(feedUpdate(
                    name=each["title"],
                    href="http://xn--80ac9aeh6f.xn--p1ai"+each["url"],
                    datetime=datetime.fromtimestamp(each["publishedAt"]).astimezone(timezone('Europe/Moscow')),
                    title=feedName))

        # custom RSS YouTube import (link to feed has to be converted manually)
        elif href.find('https://www.youtube.com/channel/') != -1:
            href = "https://www.youtube.com/feeds/videos.xml?channel_id="+href[32:-7]

            result = feedUpdate.list(feedName, href, filter)

        # default RSS import
        else:
            rss = feedparser.parse(href)

            for item in rss["items"]:
                if filter != None:
                    if item["links"][0]["href"].find(filter) == -1 and item["title_detail"]["value"].find(filter) == -1:
                        continue

                if "published" in item:
                    datestring = item["published"]
                else:
                    if "updated" in item:
                        datestring = item["updated"]

                try:
                    dateresult = datetime.strptime(datestring, '%a, %d %b %Y %H:%M:%S %z')
                except ValueError:
                    if datestring[-3] == ':':  # YouTube / TheVerge
                        dateresult = datetime.strptime(datestring[:-3] + datestring[-2:], '%Y-%m-%dT%H:%M:%S%z')
                    else:
                        try:  # except ValueError: # it is for webtooms import feeds['Gamer']
                            dateresult = datetime.strptime(datestring, '%A, %d %b %Y %H:%M:%S %Z')
                            # +timedelta(hours=3)
                        except ValueError: # it is for pikabu Brahmanden import feeds['Brahmanden']
                            try:
                                # .astimezone(timezone('UTC'))  # +timedelta(hours=3)
                                dateresult = datetime.strptime(datestring, '%a, %d %b %Y %H:%M:%S %Z')
                            except ValueError: # idea-instructions.com
                                dateresult = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S%z')

                toAdd = feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=dateresult,
                    title=feedName)
                result.append(toAdd)

        for each in result:
            # datetime fixes
            if each.datetime.tzinfo is not None and each.datetime.tzinfo.utcoffset(each.datetime) is not None:
                dateresult2 = localtime(each.datetime)
            else:
                dateresult2 = each.datetime

            del each.datetime
            each.datetime = datetime(dateresult2.year, dateresult2.month, dateresult2.day,
                dateresult2.hour, dateresult2.minute, dateresult2.second)

            # print(feed.find(feedName).delay)
            if type(feed.find(feedName).delay) is not type(None):
                dateresult = dateresult + timedelta(hours=feed.find(feedName).delay)

            # name fixes
            if each.title == 'Shadman':
                each.name = each.name[:each.name.find('(')-1]
            elif each.title == 'Apple':
                if each.name.find('— Apple') != -1:
                    each.name = each.name[:each.name.find('— Apple')]
                else:
                    each.name = each.name[:each.name.find('– Apple')]
            elif each.title == 'LastWeekTonight':
                if each.name.find(': Last Week Tonight with John Oliver (HBO)') != -1:
                    each.name = each.name[:each.name.find(': Last Week Tonight with John Oliver (HBO)')]

        return result