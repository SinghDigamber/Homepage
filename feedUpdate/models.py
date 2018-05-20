from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
import json
import urllib.request
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

        '''
    
        '': {
            'title_full': '',
            'href': ''
        },
    
        '''

    feeds = {
        # reading
        #'Система': {
        #    'title_full': 'Система Богов и Демонов',
        #    'href': 'http://xn--80ac9aeh6f.xn--p1ai/mir-boga-i-dyavola/'
        # },
        #'EvilGod': {
        #    'title_full': 'Heaven Defying Evil God',
        #    'href': 'http://xn--80ac9aeh6f.xn--p1ai/against-the-gods/'
        #},
        'EvilGodENG': {
            'title_full': 'Heaven Defying Evil God (ENG)',
            'href': 'https://www.novelupdates.com/series/against-the-gods/'
        },
        'Скульптор': {
            'title_full': 'Легендарный Лунный Скульптор',
            'href': 'http://xn--80ac9aeh6f.xn--p1ai/legendary-moonlight-sculptor/'
        },
        'Gamer': {
            'title_full': 'The Gamer',
            'href': 'feed://www.webtoons.com/en/fantasy/the-gamer/rss?title_no=88'
        },

        # YouTube
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
            'href': 'https://www.youtube.com/channel/UCuTaETsuCOkJ0H_GAztWt0Q'
        },
        'Keddr': {
            'title_full': 'Keddr.com',
            'href': 'https://www.youtube.com/channel/UCSpU8Y1aoqBSAwh8DBpiM9A'
        },
        'Kurzgesagt': {
            'title_full': 'Kurzgesagt – In a Nutshell',
            'href': 'https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q'
        },
        'LastWeekTonight': {
            'title_full': 'Last Week Tonight',
            'href': 'https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ'
        },
        'Linus': {
            'title_full': 'Linus Tech Tips',
            'href': 'https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw'
        },
        'LinusLinked': {
            'title_full': 'Linus Tech Linked',
            'href': 'https://www.youtube.com/channel/UCeeFfhMcJa1kjtfZAGskOCA'
        },
        'PRIME': {
            'title_full': 'PRIME ORCHESTRA',
            'href': 'https://www.youtube.com/channel/UCKenLkyJUXe50dVrQmLrGpw'
        },
        #'UnboxTherapy': {
        #    'title_full': 'Unbox Therapy',
        #    'href': 'https://www.youtube.com/channel/UCsTcErHg8oDvUnTzoqsYeNw'
        #},
        'Wylsa': {
            'title_full': 'Wylsacom',
            'href': 'https://www.youtube.com/channel/UCt7sv-NKh44rHAEb-qCCxvA'
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
            'title_full': 'КременюкИ',
            'href': 'https://www.youtube.com/channel/UCgLQh3fGZmfgbJ8D_sry-kA'
        },
        'Тинькофф': {
            'title_full': 'Тинькофф-Журнал',
            'href': 'https://www.youtube.com/channel/UCyYdliihJFWMXHikPK3NCQA'
        },
        'Cosplay01': {
            'title_full': 'bky guy',
            'href': 'https://www.youtube.com/channel/UCF2mFIUwbn6bANVq8xbmjdg'
        },
        'Cosplay02': {
            'title_full': 'Herzlocast',
            'href': 'https://www.youtube.com/channel/UCOCTIJiEVbSQaXeaScId_cQ'
        },
        'Астамуринг': {
            'title_full': 'Астамуринг',
            'href': 'https://www.youtube.com/channel/UCwqpU4SDWcRpL9YIuwYtF1A'
        },
        'Интервьюер': {
            'title_full': 'Зе Интервьюер',
            'href': 'https://www.youtube.com/channel/UCuWDlf53jjxti-aUA4tBdsA'
        },
        'Банкир': {
            'title_full': 'Бегущий Банкир',
            'href': 'https://www.youtube.com/channel/UCqVKtuYmKkVPaBeNFWRxlMw'
        },
        'Навальный': {
            'title_full': 'Алексей Навальный',
            'href': 'https://www.youtube.com/channel/UCsAw3WynQJMm7tMy093y37A'
        },
        'Rapha': {
            'title_full': 'Rapha Films',
            'href': 'https://www.youtube.com/channel/UCXYXxfVjxMppZY64-5baOsw'
        },
        'MarkFood': {
            'title_full': 'Mark Wiens - Hungry tourist',
            'href': 'https://www.youtube.com/channel/UCyEd6QBSgat5kkC6svyjudA'
        },
        'Kaufman': {
            'title_full': 'Ron Kaufman',
            'href': 'https://www.youtube.com/channel/UCGczcywiY2efmZ4lYb6jB9Q'
        },
        'FCade': {
            'title_full': 'Francis Cade',
            'href': 'https://www.youtube.com/channel/UCHyBWpfAggsFPDc5A7l_eWA'
        },
        'Raquel': {
            'title_full': 'Raquel Reed',
            'href': 'https://www.youtube.com/channel/UCcSow8gRPkLK0u-1pLMkZsw'
        },
        'NurkFPV': {
            'title_full': 'Nurk FPV',
            'href': 'https://www.youtube.com/channel/UCPCc4i_lIw-fW9oBXh6yTnw'
        },
        'PostMortem': {
            'title_full': 'Post-Mortem Photography',
            'href': 'https://www.youtube.com/channel/UCDFiX8wnIQwbAcnRlwSOowA'
        },
        'VergeYT': {
            'title_full': 'The Verge - YouTube',
            'href': 'https://www.youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ'
        },
        'mono': {
            'title_full': 'monobank',
            'href': 'https://www.youtube.com/channel/UClF9NLW6p4QZ28rGp8ExbAg'
        },
        'Yakushev': {
            'title_full': 'Andrei Yakushev',
            'href': 'https://www.youtube.com/channel/UCfA7eqgBGvJuBcMS8PDFjcg'
        },

        # news websites
        #'Verge': {
        #    'title_full': 'The Verge',
        #    'href': 'https://www.theverge.com/rss/index.xml'
        #}

        # shows
        'Anidub': {
            'title_full': 'Anidub online',
            'href': 'feed:https://online.anidub.com/rss.xml'
        }
    }

    def list(feedName):
        result = []

        # ранобэ.рф API import
        if feedUpdate.feeds[feedName]['href'].find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            request = "http://xn--80ac9aeh6f.xn--p1ai/v1/book/load/?book_alias="+feedUpdate.feeds[feedName]['href'][31:-1]
            request = requests.get(request).json()  # 0.4 seconds

            for part in request['result']['parts']:
                result.append(feedUpdate(
                    name=part["title"],
                    href="http://xn--80ac9aeh6f.xn--p1ai"+part["url"],
                    datetime=datetime.fromtimestamp(part["publishedAt"])-timedelta(hours=1),
                    title=feedName))

        # RSS webtoons import ( feed://www.webtoons.com/ )
        elif feedUpdate.feeds[feedName]['href'].find('feed://www.webtoons.com/') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"],'%A, %d %b %Y %H:%M:%S GMT'),
                    title=feedName))

        # RSS anidub import ( feed:https://online.anidub.com/rss.xml )
        elif feedUpdate.feeds[feedName]['href'].find('feed:https://online.anidub.com/rss.xml') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"],'%a, %d %b %Y %H:%M:%S +0300')-timedelta(hours=1),
                    title=feedName))

        # RSS TheVerge import ( https://www.theverge.com/rss/index.xml )
        elif feedUpdate.feeds[feedName]['href'].find('https://www.theverge.com/rss/index.xml') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["entries"]:
                result.append(feedUpdate(
                    name=item["title"],
                    href=item["id"],
                    datetime=datetime.strptime(item["updated"],'%Y-%m-%dT%H:%M:%S-04:00')+timedelta(hours=6),
                    title=feedName))


        # YouTube import
        elif feedUpdate.feeds[feedName]['href'].find('https://www.youtube.com/channel/') != -1:
            feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id="
                                    +feedUpdate.feeds[feedName]['href'][32:])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title"],
                    href=item["link"],
                    datetime=datetime.strptime(item["published"], '%Y-%m-%dT%H:%M:%S+00:00')+timedelta(hours=2),
                    title=feedName))

        # novelupdates.com import
        elif feedUpdate.feeds[feedName]['href'].find('https://www.novelupdates.com/series/') != -1:
            result = []
            result_name = []
            result_href = []
            result_datetime = []

            resp = requests.get(feedUpdate.feeds[feedName]['href'])  # 0.4 seconds
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
                    result_datetime.append(datetime.strptime(entry.text, "%m/%d/%y")+result_datetime_time)

            if len(result_name) == len(result_href) and len(result_href) == len(result_datetime):
                for num in range(0, len(result_name)):
                    result.append(feedUpdate(
                        name=result_name[num],
                        href=result_href[num],
                        datetime=result_datetime[num],
                        title=feedName))

        return result

    def cache():
        items = list(feedUpdate.feeds.keys())
        items = feedUpdate.multilist(items)

        for item in items:
            if not feedUpdate.objects.filter(
                name=item.name,
                href=item.href,
                # datetime=item.datetime,
                # title=item.title
            ).exists():
                #print(item)
                item.save()

    # Legacy code
    # (no longer works as AJAX is used at ранобэ.рф)
    def import_ranoberf(self):
        resp = requests.get(feedUpdate.books[book]['href'])  # 0.4 seconds
        strainer = SoupStrainer('div', attrs={'class': 'col-md-12'});
        soup = BeautifulSoup(resp.text, "html.parser")  # ~0.4 Sculptor / ~0.7 System seconds

        print(str(resp), str(soup), requests.get(feedUpdate.books[book]['href']))

        chapter_names = []
        chapter_datetimes = []
        chapter_links = []

        for entry in soup.find_all('a'):

            if str(entry).find('strong') != -1:
                chapter_names.append(entry.text)

        for entry in soup.find_all("time"):
            chapter_datetimes.append(datetime.strptime(entry.get('datetime')[:-6], "%Y-%m-%dT%H:%M:%S"))

        for entry in soup.find_all('a'):
            entry = entry.get('href')
            if type(entry) == str:
                if entry.find(feedUpdate.books[book]['href']) != -1:  # checking if link leads to the same website
                    chapter_links.append(entry)
        # chapter_links.pop(0)  # it is the button in the begging "Start reading"
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

        def import_ranoberf_api(self):
            return True

    # not needed
    #def import_youtube_alt(self):
    #    # YouTube import ALTERNATIVE (https://www.youtube.com/feeds/videos.xml?channel_id=)
    #    elif feedUpdate.feeds[feedName]['href'].find('https://www.youtube.com/feeds/videos.xml?channel_id=') != -1:
    #    feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])
    #
    #    for item in feed["items"]:
    #        result.append(feedUpdate(
    #            name=item["title"],
    #            href=item["link"],
    #            datetime=datetime.strptime(item["published"], '%Y-%m-%dT%H:%M:%S+00:00'),
    #            title=feedName))