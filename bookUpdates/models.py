from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
# Create your models here.


class chapters(models.Model):
    name = models.CharField(max_length=140)
    href = models.CharField(max_length=300)
    datetime = models.DateTimeField()
    title = models.CharField(max_length=30)

    def __init__(self, nameField, hrefField, datetimeField, titleField):
        self.name = nameField
        self.href = hrefField
        self.datetime = datetimeField
        self.title = titleField

    def multilist(items):
        chapters.cache()
        result = []
        for item in items:
            result.extend(chapters.list(item))

        return result

    books = {
        'Система': {
            'title_full': 'Система Богов и Демонов',
            'href': 'http://xn--80ac9aeh6f.xn--p1ai/mir-boga-i-dyavola/'},
        'Скульптор': {
            'title_full': 'Легендарный Лунный Скульптор',
            'href': 'http://xn--80ac9aeh6f.xn--p1ai/legendary-moonlight-sculptor/'},
        'Gamer': {
            'title_full': 'The Gamer',
            'href': 'feed://www.webtoons.com/en/fantasy/the-gamer/rss?title_no=88'
        },
    }

    def list(book):
        result = []
        timeDiff = 2  # difference from UTC

        # ранобэ.рф import
        if chapters.books[book]['href'].find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            resp = requests.get(chapters.books[book]['href'])  # 0.4 seconds
            strainer = SoupStrainer('div', attrs={'class': 'col-md-12'});
            soup = BeautifulSoup(resp.text, "lxml", parse_only=strainer)  # ~0.4 Sculptor / ~0.7 System seconds

            chapter_names = []
            chapter_datetimes = []
            chapter_links = []

            for entry in soup.find_all('a'):
                if str(entry).find('Глава') != -1:
                    chapter_names.append(entry.text)

            for entry in soup.find_all("time"):
                chapter_datetimes.append(datetime.strptime(entry.get('datetime')[:-6], "%Y-%m-%dT%H:%M:%S")+timedelta(hours=timeDiff))

            for entry in soup.find_all('a'):
                entry = entry.get('href')
                if type(entry) == str:
                    if entry.find(chapters.books[book]['href']) != -1:  # checking if link leads to the same website
                        chapter_links.append(entry)
            #chapter_links.pop(0)  # it is the button in the begging "Start reading"
            chapter_links = list(OrderedDict((x, True) for x in chapter_links).keys())  # allow unique links only

            if len(chapter_links) == len(chapter_names) and len(chapter_names) == len(chapter_datetimes):
                for i in range(0, len(chapter_links)):
                    result.append(chapters(str(chapter_names[i]), str(chapter_links[i]), str(chapter_datetimes[i]), book))

            else:
                print("Number of links (%(links)s) do not match titles (%(names)s) and datetimes (%(datetimes)s)"
                    % {'links': len(chapter_links), 'names': len(chapter_names), 'datetimes': len(chapter_datetimes)})

        # RSS import (feed://www.webtoons.com/)
        elif chapters.books[book]['href'].find('feed://') != -1:
            feed = feedparser.parse(chapters.books[book]['href'])

            for item in feed["items"]:
                result.append(chapters(item["title_detail"]["value"], item["links"][0]["href"],
                    datetime.strptime(item["published"],
                    '%A, %d %b %Y %H:%M:%S GMT')+timedelta(hours=timeDiff), book))



        return result

    def cache():
        #return False
        keys = list(chapters.books.keys())
        all = chapters.multilist(keys)

        for item in all:
            item.save()