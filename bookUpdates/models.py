from django.db import models
from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
import datetime
import time
import lxml

# Create your models here.


class chapters(models.Model):
    def __init__(self, name, href, datetime, title):
        self.name = name
        self.href = href
        #self.datetime = datetime.datetime.strptime(datetime1, '%Y-%m-%dT%H:%M:%S+00:00')
        self.datetime = datetime[:10]
        self.title = title

    def log(log):
        print(log)

    def multilist(items):
        #start = time.time()
        result = []
        for item in items:
            result.extend(chapters.list(item))
        #print("TOTAL: ", time.time() - start)
        return result

    books = {
        'Система': {
            'title_full': 'Система Богов и Демонов',
            'href': 'http://xn--80ac9aeh6f.xn--p1ai/mir-boga-i-dyavola/'},
        'Скульптор': {
            'title_full': 'Легендарный Лунный Скульптор',
            'href': 'http://xn--80ac9aeh6f.xn--p1ai/legendary-moonlight-sculptor/'},
    }

    def list(book):
        # ранобэ.рф import
        if chapters.books[book]['href'].find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            resp = requests.get(chapters.books[book]['href'])  # 0.4 seconds
            soup = BeautifulSoup(resp.text, "lxml")  # ~0.4 Sculptor / ~0.7 System seconds

            chapter_names = []
            for entry in soup.find_all('a'):
                if str(entry).find('Глава') != -1:
                    chapter_names.append(entry.text)

            chapter_datetimes = []
            for entry in soup.find_all("time"):
                chapter_datetimes.append(entry.get('datetime'))

            chapter_links = []
            for entry in soup.find_all('a'):
                entry = entry.get('href')
                if type(entry) == str:
                    if entry.find(chapters.books[book]['href']) != -1:  # checking if link leads to the same website
                        chapter_links.append(entry)
            chapter_links.pop(0)  # it is the button in the begging "Start reading"
            chapter_links = list(OrderedDict((x, True) for x in chapter_links).keys())  # allow unique links only
            result = []
            if len(chapter_links) == len(chapter_names) and len(chapter_names) == len(chapter_datetimes):
                for i in range(0, len(chapter_links)):
                    result.append(chapters(str(chapter_names[i]), str(chapter_links[i]), str(chapter_datetimes[i]), book))

            else:
                chapters.log("Number of links (%(links)s) do not match titles (%(names)s) and datetimes (%(datetimes)s)"
                             % {'links': len(chapter_links), 'names': len(chapter_names),
                                'datetimes': len(chapter_datetimes)})

        return result
