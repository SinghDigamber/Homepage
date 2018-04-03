from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
# Create your models here.


class feedUpdate(models.Model):
    class Meta:
        ordering = ['-datetime']
    name = models.CharField(max_length=140)
    href = models.CharField(max_length=300)
    datetime = models.DateTimeField()
    title = models.CharField(max_length=30)

    def __str__(self):
        return "["+self.title+"] - "+self.name+" on "+str(self.datetime)+" link: "+self.href

    def multilist(items):
        result = []
        for item in items:
            result.extend(feedUpdate.list(item))

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
        'Ляпота': {
            'title_full': "It's a good trip",
            'href': 'https://www.youtube.com/channel/UCeHB0mXXj_kyPCB-yRr8b9w'
        },
        'GCNTech': {
            'title_full': "GCN Tech",
            'href': 'https://www.youtube.com/channel/UC710HJmp-YgNbE5BnFBRoeg'
        },
        'GCN': {
            'title_full': "Global Cycling Network",
            'href': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCuTaETsuCOkJ0H_GAztWt0Q'
        },
        'Keddr': {
            'title_full': 'Keddr.com',
            'href': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCSpU8Y1aoqBSAwh8DBpiM9A',
        },
        'Kurzgesagt': {
            'title_full': 'Kurzgesagt – In a Nutshell',
            'href': 'https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q',
        },
        'LastWeekTonight': {
            'title_full': 'Last Week Tonight',
            'href': 'https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ',
        },
        'Linus': {
            'title_full': 'Linus Tech Tips',
            'href': 'https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw',
        },
        'PRIME': {
            'title_full': 'PRIME ORCHESTRA',
            'href': 'https://www.youtube.com/channel/UCKenLkyJUXe50dVrQmLrGpw',
        },
        'UnboxTherapy': {
            'title_full': 'Unbox Therapy',
            'href': 'https://www.youtube.com/channel/UCsTcErHg8oDvUnTzoqsYeNw',
        },
        'Wylsa': {
            'title_full': 'Wylsacom',
            'href': 'https://www.youtube.com/channel/UCt7sv-NKh44rHAEb-qCCxvA',
        },
        'Jannet': {
            'title_full': 'Jannet Incosplay',
            'href': 'https://www.youtube.com/channel/UCr2dfQlDaZlqpAPv_TKYSdQ'
        },
        'Nigri': {
            'title_full': 'Jessica Nigri',
            'href': 'https://www.youtube.com/channel/UCTg4jls4URruaHauposrhMg'
        },
        'КременюкИ': {
            'title_full': 'Jessica Nigri',
            'href': 'https://www.youtube.com/channel/UCgLQh3fGZmfgbJ8D_sry-kA'
        },
    }

    def list(book):
        result = []
        timeDiff=3

        # ранобэ.рф import
        if feedUpdate.books[book]['href'].find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            resp = requests.get(feedUpdate.books[book]['href'])  # 0.4 seconds
            strainer = SoupStrainer('div', attrs={'class': 'col-md-12'});
            soup = BeautifulSoup(resp.text, "lxml", parse_only=strainer)  # ~0.4 Sculptor / ~0.7 System seconds

            chapter_names = []
            chapter_datetimes = []
            chapter_links = []

            for entry in soup.find_all('a'):
                if str(entry).find('Глава') != -1:
                    chapter_names.append(entry.text)

            for entry in soup.find_all("time"):
                chapter_datetimes.append(datetime.strptime(entry.get('datetime')[:-6], "%Y-%m-%dT%H:%M:%S"))

            for entry in soup.find_all('a'):
                entry = entry.get('href')
                if type(entry) == str:
                    if entry.find(feedUpdate.books[book]['href']) != -1:  # checking if link leads to the same website
                        chapter_links.append(entry)
            #chapter_links.pop(0)  # it is the button in the begging "Start reading"
            chapter_links = list(OrderedDict((x, True) for x in chapter_links).keys())  # allow unique links only

            if len(chapter_links) == len(chapter_names) and len(chapter_names) == len(chapter_datetimes):
                for i in range(0, len(chapter_links)):
                    result.append(feedUpdate(
                        name=str(chapter_names[i]),
                        href=str(chapter_links[i]),
                        datetime=str(chapter_datetimes[i]),
                        title=book))

            else:
                print("Number of links (%(links)s) do not match titles (%(names)s) and datetimes (%(datetimes)s)"
                    % {'links': len(chapter_links), 'names': len(chapter_names), 'datetimes': len(chapter_datetimes)})

        # RSS import (feed://www.webtoons.com/)
        elif feedUpdate.books[book]['href'].find('feed://') != -1:
            feed = feedparser.parse(feedUpdate.books[book]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"],'%A, %d %b %Y %H:%M:%S GMT')+timedelta(hours=timeDiff),
                    title=book))

        # YouTube import (https://www.youtube.com/feeds/videos.xml?channel_id=)
        elif feedUpdate.books[book]['href'].find('https://www.youtube.com/channel/') != -1:

            feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id="
                                    +feedUpdate.books[book]['href'][32:])

            for item in feed["items"]:

                result.append(feedUpdate(
                    name=item["title"],
                    href=item["link"],
                    datetime=datetime.strptime(item["published"], '%Y-%m-%dT%H:%M:%S+00:00'),
                    title=book))

        # YouTube import ALTERNATIVE (https://www.youtube.com/feeds/videos.xml?channel_id=)
        elif feedUpdate.books[book]['href'].find('https://www.youtube.com/feeds/videos.xml?channel_id=') != -1:
            feed = feedparser.parse(feedUpdate.books[book]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title"],
                    href=item["link"],
                    datetime=datetime.strptime(item["published"], '%Y-%m-%dT%H:%M:%S+00:00'),
                    title=book))

        return result

    def cache():
        #return False
        result = 0;
        items = list(feedUpdate.books.keys())
        items = feedUpdate.multilist(items)

        for item in items:
            if not feedUpdate.objects.filter(
                name=item.name,
                href=item.href,
                datetime=item.datetime,
                title=item.title
            ).exists():
                #print(item)
                item.save()
                result += 1

        #print(result)
