from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
import json
import urllib.request
# Create your models here.

class feed(models.Model):
    #class Meta:
    #    ordering = ['href']
    title = models.CharField(max_length=42)
    title_full = models.CharField(max_length=140)
    href = models.CharField(max_length=300)

    emojis = models.CharField(max_length=140)
    status = models.CharField(max_length=140)  # options



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
            try:
                result.extend(feedUpdate.list(item))
            except KeyError:
                result.append(feedUpdate(
                    name="not found in feeds",
                    href="#",
                    datetime=datetime.now()+timedelta(hours=-3),
                    title=item))
                print("item: not found in feeds")

        return result

    feeds = {
        'EvilGod': {
            'title_full': 'Heaven Defying Evil God',
            'href': 'https://www.novelupdates.com/series/against-the-gods/'
        },
        'Renegade': {
            'title_full': 'Renegade Immortal',
            'href': 'https://www.novelupdates.com/series/renegade-immortal/'
        },
        'Скульптор': {
            'title_full': 'Легендарный Лунный Скульптор',
            'href': 'http://xn--80ac9aeh6f.xn--p1ai/legendary-moonlight-sculptor/'
        },
        'Gamer': {
            'title_full': 'The Gamer',
            'href': 'feed://www.webtoons.com/en/fantasy/the-gamer/rss?title_no=88'
        },
        'Ляпота': {
            'title_full': "It's a good trip",
            'href': 'https://www.youtube.com/channel/UCeHB0mXXj_kyPCB-yRr8b9w/videos'
        },
        'GCNTech': {
            'title_full': "GCN Tech",
            'href': 'https://www.youtube.com/channel/UC710HJmp-YgNbE5BnFBRoeg/videos'
        },
        'GCN': {
            'title_full': "Global Cycling Network",
            'href': 'https://www.youtube.com/channel/UCuTaETsuCOkJ0H_GAztWt0Q/videos'
        },
        'Keddr': {
            'title_full': 'Keddr.com',
            'href': 'https://www.youtube.com/channel/UCSpU8Y1aoqBSAwh8DBpiM9A/videos'
        },
        'Kurzgesagt': {
            'title_full': 'Kurzgesagt – In a Nutshell',
            'href': 'https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q/videos'
        },
        'LastWeekTonight': {
            'title_full': 'Last Week Tonight',
            'href': 'https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ/videos'
        },
        'Linus': {
            'title_full': 'Linus Tech Tips',
            'href': 'https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw/videos'
        },
        'TechLinked': {
            'title_full': 'Tech Linked',
            'href': 'https://www.youtube.com/channel/UCeeFfhMcJa1kjtfZAGskOCA/videos'
        },
        'PRIME': {
            'title_full': 'PRIME ORCHESTRA',
            'href': 'https://www.youtube.com/channel/UCKenLkyJUXe50dVrQmLrGpw/videos'
        },
        #'UnboxTherapy': {
        #    'title_full': 'Unbox Therapy',
        #    'href': 'https://www.youtube.com/channel/UCsTcErHg8oDvUnTzoqsYeNw/videos'
        #},
        'Wylsa': {
            'title_full': 'Wylsacom',
            'href': 'https://www.youtube.com/channel/UCt7sv-NKh44rHAEb-qCCxvA/videos'
        },
        'Jannet': {
            'title_full': 'Jannet Incosplay',
            'href': 'https://www.youtube.com/channel/UCr2dfQlDaZlqpAPv_TKYSdQ/videos'
        },
        'Nigri': {
            'title_full': 'Jessica Nigri',
            'href': 'https://www.youtube.com/channel/UCTg4jls4URruaHauposrhMg/videos'
        },
        'КременюкИ': {
            'title_full': 'КременюкИ',
            'href': 'https://www.youtube.com/channel/UCgLQh3fGZmfgbJ8D_sry-kA/videos'
        },
        'Тинькофф': {
            'title_full': 'Тинькофф-Журнал',
            'href': 'https://www.youtube.com/channel/UCyYdliihJFWMXHikPK3NCQA/videos'
        },
        #'Cosplay01': {
        #    'title_full': 'bky guy',
        #    'href': 'https://www.youtube.com/channel/UCF2mFIUwbn6bANVq8xbmjdg/videos'
        #},
        #'Cosplay02': {
        #    'title_full': 'Herzlocast',
        #    'href': 'https://www.youtube.com/channel/UCOCTIJiEVbSQaXeaScId_cQ/videos'
        #},
        'Астамуринг': {
            'title_full': 'Астамуринг',
            'href': 'https://www.youtube.com/channel/UCwqpU4SDWcRpL9YIuwYtF1A/videos'
        },
        'Интервьюер': {
            'title_full': 'Зе Интервьюер',
            'href': 'https://www.youtube.com/channel/UCuWDlf53jjxti-aUA4tBdsA/videos'
        },
        #'Банкир': {
        #    'title_full': 'Бегущий Банкир',
        #    'href': 'https://www.youtube.com/channel/UCqVKtuYmKkVPaBeNFWRxlMw/videos'
        #},
        'Навальный': {
            'title_full': 'Алексей Навальный',
            'href': 'https://www.youtube.com/channel/UCsAw3WynQJMm7tMy093y37A/videos'
        },
        'Rapha': {
            'title_full': 'Rapha Films',
            'href': 'https://www.youtube.com/channel/UCXYXxfVjxMppZY64-5baOsw/videos'
        },
        'MarkFood': {
            'title_full': 'Mark Wiens - Hungry tourist',
            'href': 'https://www.youtube.com/channel/UCyEd6QBSgat5kkC6svyjudA/videos'
        },
        'Kaufman': {
            'title_full': 'Ron Kaufman',
            'href': 'https://www.youtube.com/channel/UCGczcywiY2efmZ4lYb6jB9Q/videos'
        },
        'FCade': {
            'title_full': 'Francis Cade',
            'href': 'https://www.youtube.com/channel/UCHyBWpfAggsFPDc5A7l_eWA/videos'
        },
        'Raquel': {
            'title_full': 'Raquel Reed',
            'href': 'https://www.youtube.com/channel/UCcSow8gRPkLK0u-1pLMkZsw/videos'
        },
        'NurkFPV': {
            'title_full': 'Nurk FPV',
            'href': 'https://www.youtube.com/channel/UCPCc4i_lIw-fW9oBXh6yTnw/videos'
        },
        'PostMortem': {
            'title_full': 'Post-Mortem Photography',
            'href': 'https://www.youtube.com/channel/UCDFiX8wnIQwbAcnRlwSOowA/videos'
        },
        'VergeYT': {
            'title_full': 'The Verge - YouTube',
            'href': 'https://www.youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ/videos'
        },
        'mono': {
            'title_full': 'monobank',
            'href': 'https://www.youtube.com/channel/UClF9NLW6p4QZ28rGp8ExbAg/videos'
        },
        'Yakushev': {
            'title_full': 'Andrei Yakushev',
            'href': 'https://www.youtube.com/channel/UCfA7eqgBGvJuBcMS8PDFjcg/videos'
        },
        "ПланетаКино": {
            'title_full': "Планета Кино",
            'href': 'https://www.youtube.com/channel/UCrR7GJSvz481CxHQn-yXHJw/videos'
        },
        "MLewin": {
            'title_full': "Michelle Lewin",
            'href': "https://www.youtube.com/channel/UCXOF8RQ_v52K1uq6m_rMy1w/videos"
        },
        "AdventureTeam": {
            'title_full': "Adventure Team",
            'href': "https://www.youtube.com/channel/UCnusq0cEepVKVAlftFn8u5Q/videos"
        },
        "OverwatchRU": {
            'title_full': "Overwatch RU",
            'href': "https://www.youtube.com/channel/UCpW84gDcZu8wNQ-tUO5qE6A/videos"
        },
        "cherrycrush": {
            'title_full': "My Cherry Crush",
            'href': "https://www.youtube.com/channel/UC4lkVwG5XViZuoRrjdUqEeA/videos"
        },
        "Cosplay03": {
            'title_full': "Milligan Vick",
            'href': "https://www.youtube.com/channel/UCPi1NLlECKm4VGpNjDUiBmg/videos"
        },
        "Snazzy": {
            'title_full': "Snazzy Labs",
            'href': "https://www.youtube.com/channel/UCO2x-p9gg9TLKneXlibGR7w/videos"
        },
        'Хач': {
            'title_full': 'ДНЕВНИК ХАЧА',
            'href': 'https://www.youtube.com/channel/UCnbxcA3kZ_uUYIBHNvxpDQw/videos'
        },
        'ЧумацкийВелопробег': {
            'title_full': 'Чумацкий путь в Америку - велопробег',
            'href': 'https://www.youtube.com/channel/UC4d-CwWxC8i96D9mKAAtnbA/videos'
        },
        'Шелягина': {
            'title_full': 'Наташа Шелягина',
            'href': 'https://www.youtube.com/channel/UC97y3hRp4lfOhAZpuSbYruQ/videos'
        },
        'GMBNTech': {
            'title_full': 'GMBN Tech',
            'href': 'https://www.youtube.com/channel/UC6juisijUAHcJLt23nk-qOQ/videos'
        },
        'GMBN': {
            'title_full': 'GMBN',
            'href': 'https://www.youtube.com/channel/UC_A--fhX5gea0i4UtpD99Gg/videos'
        },
        'ArhyBES': {
            'title_full': 'ArhyBES',
            'href': 'https://www.youtube.com/channel/UCby5ZKyxiSW3dz_Kg5VDU9w/videos'
        },
        'Blackpack': {
            'title_full': 'Blackpack',
            'href': 'https://www.youtube.com/channel/UChXHexCL-d0538NwLClRDJQ/videos'
        },
        'Сыендук': {
            'title_full': 'Сыендук',
            'href': 'https://www.youtube.com/channel/UC-b89a0Fw6pNoP-g-_qLeiw/videos'
        },
        'Veddro': {
            'title_full': 'Veddro.com',
            'href': 'https://www.youtube.com/channel/UCItSim1k6hOHyogg1LJ0JCQ/videos'
        },
        'Ленинград': {
            'title_full': 'Ленинград',
            'href': 'https://www.youtube.com/channel/UCY0C6A3t3RTUN3BB65rWAgQ/videos'
        },
        'BadComedian': {
            'title_full': '[BadComedian]',
            'href': 'https://www.youtube.com/channel/UC6cqazSR6CnVMClY0bJI0Lg/videos'
        },
        'MKBHD': {
            'title_full': 'Marques Brownlee',
            'href': 'https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ/videos'
        },
        'Corridor': {
            'title_full': 'Corridor Digital',
            'href': 'https://www.youtube.com/channel/UCsn6cjffsvyOZCZxvGoJxGg/videos'
        },
        'KymNonStop': {
            'title_full': 'KymNonStop',
            'href': 'https://www.youtube.com/channel/UCM6cd0hPii_FJOzZaxqGj7w/videos'
        },
        'devinsupertramp': {
            'title_full': 'devinsupertramp',
            'href': 'https://www.youtube.com/channel/UCwgURKfUA7e0Z7_qE3TvBFQ/videos'
        },
        'IFHT': {
            'title_full': 'IFHT Films',
            'href': 'https://www.youtube.com/channel/UCTs59UCfP4YLUt6pDR_uLtg/videos'
        },
        'Relaxation4K': {
            'title_full': '4K Relaxation Channel',
            'href': 'https://www.youtube.com/channel/UCg72Hd6UZAgPBAUZplnmPMQ/videos'
        },
        'LazySquare': {
            'title_full': 'Lazy Square',
            'href': 'https://www.youtube.com/channel/UCZTc2bbF64cj_r0btHgaakw/videos'
        },
        'Zaddrot': {
            'title_full': 'Zaddrot',
            'href': 'https://www.youtube.com/channel/UCjQb9npdMq_u1rRBgoQ24fg/videos'
        },
        'Notordinarytravel': {
            'title_full': 'Get out from the ordinary travel ',
            'href': 'https://www.youtube.com/channel/UCY5X52SAYFz3nejVwvjf9gg/videos'
        },

        

        # shows
        'Anidub': {
            'title_full': 'Anidub Online',
            'href': 'feed:https://online.anidub.com/rss.xml'
        },
        'Gam3': {
            'title_full': 'The Gam3',
            'href': 'feed:https://thegam3.com/feed/'
        },
        'Jago': {
            'title_full': 'Jagodibuja',
            'href': 'feed://www.jagodibuja.com/feed/'
        },
        'vas3k': {
            'title_full': 'vas3k.ru',
            'href': 'feed:https://vas3k.ru/rss/'
        },
        'DisgustingMen': {
            'title_full': 'Disgusting Men',
            'href': 'feed:https://disgustingmen.com/feed/'
        },
        'XKCD': {
            'title_full': 'XKCD',
            'href': 'https://xkcd.com/rss.xml'
        },
        #'КабМин': {
        #    'title_full': 'Кабинет Министров Украины',
        #    'href': 'https://www.kmu.gov.ua/api/rss'
        #},
        'Reflective': {
            'title_full': 'Reflective Desire',
            'href': 'feed:https://reflectivedesire.com/rss/'
        },
        # 'Verge':{'title_full':'The Verge','href':'https://www.theverge.com/rss/index.xml'},
    }

    def list(feedName):
        result = []

        # ранобэ.рф API import
        # TODO: stupid workaround as API will be closed
        if feedUpdate.feeds[feedName]['href'].find('http://xn--80ac9aeh6f.xn--p1ai/') != -1:
            request = "https://xn--80ac9aeh6f.xn--p1ai/v1/book/get/?bookAlias="+feedUpdate.feeds[feedName]['href'][31:-1]
            request = requests.get(request).json()  # 0.4 seconds

            for each in request['result']['parts']:
                result.append(feedUpdate(
                    name=each["title"],
                    href="http://xn--80ac9aeh6f.xn--p1ai"+each["url"],
                    datetime=datetime.fromtimestamp(each["publishedAt"])+timedelta(hours=1),
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

        # RSS YouTube import
        elif feedUpdate.feeds[feedName]['href'].find('https://www.youtube.com/channel/') != -1:
            feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id="
                +feedUpdate.feeds[feedName]['href'][32:-7])

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

        # RSS TheGam3.com import
        elif feedUpdate.feeds[feedName]['href'].find('feed:https://thegam3.com/feed/') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S +0000'),
                    title=feedName))

        # RSS jagodibuja import
        elif feedUpdate.feeds[feedName]['href'].find('feed://www.jagodibuja.com/feed/') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S +0000'),
                    title=feedName))

        # RSS vas3k.ru import
        elif feedUpdate.feeds[feedName]['href'].find('feed:https://vas3k.ru/rss/') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S +0000'),
                    title=feedName))

        # RSS disgustingmen.com import
        elif feedUpdate.feeds[feedName]['href'].find('feed:https://disgustingmen.com/feed/') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S +0000'),
                    title=feedName))

        # RSS xkcd.com import
        elif feedUpdate.feeds[feedName]['href'].find('https://xkcd.com/rss.xml') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S -0000'),
                    title=feedName))

        # RSS kmu.gov.ua import
        elif feedUpdate.feeds[feedName]['href'].find('https://www.kmu.gov.ua/api/rss') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S +0300'),
                    title=feedName))

        # RSS reflectivedesire.com import
        elif feedUpdate.feeds[feedName]['href'].find('eflectivedesire.com/rss/') != -1:
            feed = feedparser.parse(feedUpdate.feeds[feedName]['href'])

            for item in feed["items"]:
                result.append(feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S -0700'),
                    title=feedName))

        # RSS reflectivedesire.com import manual workaround
        ''' elif feedUpdate.feeds[feedName]['href'].find('reflectivedesire.com/rss/') != -1:
            try:
                resp = requests.get(feedUpdate.feeds[feedName]['href'])
                soup = BeautifulSoup(resp.text, "html.parser")

                log = feedUpdate(
                    name="SUCCESS",
                    href="#",
                    datetime=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    title=feedName)
                log.save()
                #result.append(log)
                #print(log)

                for each in soup.find_all("item"):
                    result.append(feedUpdate(
                        name=each.find("title").string,
                        href=each.find("guid").string,
                        datetime=datetime.strptime(each.find("pubdate").string, '%a, %d %b %Y %H:%M:%S -0700'),
                        title=feedName))
            except requests.exceptions.ConnectionError:
                print("feedUpdate/feeds/Reflective: Connection refused") '''

        return result

    def cache():
        items = list(feedUpdate.feeds.keys())
        items = feedUpdate.multilist(items)

        for item in items:
            if not feedUpdate.objects.filter(
                # name=item.name,
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
