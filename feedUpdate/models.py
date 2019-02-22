from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
from pytz import timezone
# Create your models here.

# TODO: move project to actual database



# emojis
# 🏮 - hide from fU/feeds
# 💎 - inIndex=True


class feed(models.Model):
    class Meta:
        ordering = ['title_full']
    title = models.CharField(max_length=42)
    title_full = models.CharField(max_length=140)
    href = models.CharField(max_length=420)
    href_title = models.CharField(max_length=420)
    emojis = models.CharField(max_length=7)  # usage as tags
    filter = models.CharField(max_length=140)
    delay = models.IntegerField()

    def find(title):
        for item in feeds:
            if item.title == title:
                return item

    def keys():
        result = []
        for item in feeds:
            if item.emojis.find('💎') != -1:
                result.append(item.title)
        return result

    def keysAll():
        result = []
        for item in feeds:
            result.append(item.title)
        return result

    def all():
        return feeds


from .feeds import feeds


class feedUpdate(models.Model):
    class Meta:
        ordering = ['-datetime']
    name = models.CharField(max_length=140)
    href = models.CharField(max_length=210)
    datetime = models.DateTimeField()
    title = models.CharField(max_length=42)

    def __str__(self):
        return "["+self.title+"] "+self.name+" published on "+str(self.datetime)+" with link "+self.href

    def multilist(items):
        # TODO: merge forced and not algorithms and do everything via this function
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
        # TODO: stupid workaround as API will be closed (can be ignored ATM)
        if href.find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            request = "https://xn--80ac9aeh6f.xn--p1ai/v1/book/get/?bookAlias="+href[31:-1]
            request = requests.get(request).json()  # 0.4 seconds

            for each in request['result']['parts']:
                result.append(feedUpdate(
                    name=each["title"],
                    href="http://xn--80ac9aeh6f.xn--p1ai"+each["url"],
                    # TODO: check timezone as it is unknown (current theory is Moscow time):
                    datetime=datetime.fromtimestamp(each["publishedAt"]).astimezone(timezone('Europe/Kiev')),
                    title=feedName))

        # custom RSS YouTube import (link to feed has to be converted manually)
        elif href.find('https://www.youtube.com/channel/') != -1:
            href = "https://www.youtube.com/feeds/videos.xml?channel_id="+href[32:-7]

            result = feedUpdate.list(feedName, href, filter)

        # custom novelupdates.com import
        elif href.find('https://www.novelupdates.com/series/') != -1:
            result = []
            result_name = []
            result_href = []
            result_datetime = []

            resp = requests.get(href)  # 0.4 seconds
            strainer = SoupStrainer('table', attrs={'id': 'myTable'});
            soup = BeautifulSoup(resp.text, "lxml", parse_only=strainer)  # ~0.4 Sculptor / ~0.7 System seconds

            for entry in soup.find_all(attrs={"class": "chp-release"}):
                result_name.append("Chapter "+entry['title'][1:])
                result_href.append("http:"+entry['href'])

            for entry in soup.find_all(attrs={"style": "padding-left:5px;"}):
                if entry.text != "Date":
                    result_datetime_time=timedelta(
                        hours=datetime.now().hour,
                        minutes=datetime.now().minute,
                        seconds=datetime.now().second)
                    #if datetime.now().hour <= 12:
                    #    result_datetime_time = result_datetime_time+timedelta(days=1)
                    # +timedelta(hours=3)

                    result_datetime_time = datetime.strptime(entry.text, "%m/%d/%y")+result_datetime_time
                    result_datetime_time = result_datetime_time + timedelta(hours=24)
                    # result_datetime_time = datetime.now()
                    result_datetime_time.astimezone(timezone('Europe/Kiev'))
                    result_datetime.append(result_datetime_time)

            if len(result_name) == len(result_href) and len(result_href) == len(result_datetime):
                for num in range(0, len(result_name)):
                    result.append(feedUpdate(
                        name=result_name[num],
                        href=result_href[num],
                        datetime=result_datetime[num],
                        title=feedName))

        # default RSS import
        else:
            rss = feedparser.parse(href)

            for item in rss["items"]:
                if item["links"][0]["href"].find(filter) != -1 or item["title_detail"]["value"].find(filter) != -1:
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

                    delay=feed.find(feedName).delay
                    if(type(delay) is not type(None)):
                        dateresult = dateresult + timedelta(hours=delay)

                    toAdd = feedUpdate(
                        name=item["title_detail"]["value"],
                        href=item["links"][0]["href"],
                        datetime=dateresult,
                        title=feedName)
                    result.append(toAdd)

        return result
