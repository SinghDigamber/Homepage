from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
from collections import OrderedDict
import feedparser
from datetime import datetime, timedelta
from pytz import timezone
# Create your models here.

# TODO: move project to actual database

class feed(models.Model):
    class Meta:
        ordering = ['title_full']
    title = models.CharField(max_length=42)
    title_full = models.CharField(max_length=140)
    href = models.CharField(max_length=420)
    href_title = models.CharField(max_length=420)
    emojis = models.CharField(max_length=7)  # usage as tags
    inIndex = models.BooleanField(default=True)  # showing feed in feedUpdate

    def find(title):
        for item in feeds:
            if item.title == title:
                return item

    def keys():
        result = []
        for item in feeds:
            if (item.inIndex==True):
                result.append(item.title)
        return result

    def keysAll():
        result = []
        for item in feeds:
            result.append(item.title)
        return result

    def all():
        return feeds


feeds = [
        feed(
            title='Скульптор',
            title_full='Легендарный Лунный Скульптор',
            href='http://xn--80ac9aeh6f.xn--p1ai/legendary-moonlight-sculptor/',
            href_title='http://xn--80ac9aeh6f.xn--p1ai/legendary-moonlight-sculptor/',
            emojis='',
            inIndex=True
        ),
        feed(
            title='RenegadeImmortal',
            title_full='Renegade Immortal',
            href='https://www.novelupdates.com/series/renegade-immortal/',
            href_title='https://www.wuxiaworld.com/novel/renegade-immortal',
            emojis='',
            inIndex=True
        ),
        feed(
            title='EvilGod',
            title_full='Heaven Defying Evil God',
            href='https://www.novelupdates.com/series/against-the-gods/',
            href_title='https://www.wuxiaworld.com/novel/against-the-gods',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Gamer',
            title_full='The Gamer',
            href='feed://www.webtoons.com/en/fantasy/the-gamer/rss?title_no=88',
            href_title='https://www.webtoons.com/en/fantasy/the-gamer/list?title_no=88&page=1',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Ляпота',
            title_full="It's a good trip",
            href='https://www.youtube.com/channel/UCeHB0mXXj_kyPCB-yRr8b9w/videos',
            href_title='https://www.youtube.com/channel/UCeHB0mXXj_kyPCB-yRr8b9w/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='GCNTech',
            title_full="GCN Tech",
            href='https://www.youtube.com/channel/UC710HJmp-YgNbE5BnFBRoeg/videos',
            href_title='https://www.youtube.com/channel/UC710HJmp-YgNbE5BnFBRoeg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='GCN',
            title_full="Global Cycling Network",
            href='https://www.youtube.com/channel/UCuTaETsuCOkJ0H_GAztWt0Q/videos',
            href_title='https://www.youtube.com/channel/UCuTaETsuCOkJ0H_GAztWt0Q/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Keddr',
            title_full='Keddr.com',
            href='https://www.youtube.com/channel/UCSpU8Y1aoqBSAwh8DBpiM9A/videos',
            href_title='https://www.youtube.com/channel/UCSpU8Y1aoqBSAwh8DBpiM9A/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Kurzgesagt',
            title_full='Kurzgesagt – In a Nutshell',
            href='https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q/videos',
            href_title='https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='LastWeekTonight',
            title_full='Last Week Tonight with John Oliver',
            href='https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ/videos',
            href_title='https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Linus',
            title_full='Linus Tech Tips',
            href='https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw/videos',
            href_title='https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='TechLinked',
            title_full='Tech Linked by Linus',
            href='https://www.youtube.com/channel/UCeeFfhMcJa1kjtfZAGskOCA/videos',
            href_title='https://www.youtube.com/channel/UCeeFfhMcJa1kjtfZAGskOCA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='PRIME',
            title_full='PRIME ORCHESTRA',
            href='https://www.youtube.com/channel/UCKenLkyJUXe50dVrQmLrGpw/videos',
            href_title='https://www.youtube.com/channel/UCKenLkyJUXe50dVrQmLrGpw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='UnboxTherapy',
            title_full='Unbox Therapy',
            href='https://www.youtube.com/channel/UCsTcErHg8oDvUnTzoqsYeNw/videos',
            href_title='https://www.youtube.com/channel/UCsTcErHg8oDvUnTzoqsYeNw/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Wylsa',
            title_full='Wylsacom',
            href='https://www.youtube.com/channel/UCt7sv-NKh44rHAEb-qCCxvA/videos',
            href_title='https://www.youtube.com/channel/UCt7sv-NKh44rHAEb-qCCxvA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Jannet',
            title_full='Jannet Incosplay',
            href='https://www.youtube.com/channel/UCr2dfQlDaZlqpAPv_TKYSdQ/videos',
            href_title='https://www.youtube.com/channel/UCr2dfQlDaZlqpAPv_TKYSdQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Nigri',
            title_full='Jessica Nigri',
            href='https://www.youtube.com/channel/UCTg4jls4URruaHauposrhMg/videos',
            href_title='https://www.youtube.com/channel/UCTg4jls4URruaHauposrhMg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='КременюкИ',
            title_full='КременюкИ',
            href='https://www.youtube.com/channel/UCgLQh3fGZmfgbJ8D_sry-kA/videos',
            href_title='https://www.youtube.com/channel/UCgLQh3fGZmfgbJ8D_sry-kA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Т—Ж',
            title_full='Тинькофф-Журнал (YouTube)',
            href='https://www.youtube.com/channel/UCyYdliihJFWMXHikPK3NCQA/videos',
            href_title='https://www.youtube.com/channel/UCyYdliihJFWMXHikPK3NCQA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Cosplay01',
            title_full='bky guy',
            href='https://www.youtube.com/channel/UCF2mFIUwbn6bANVq8xbmjdg/videos',
            href_title='https://www.youtube.com/channel/UCF2mFIUwbn6bANVq8xbmjdg/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Cosplay02',
            title_full='Herzlocast',
            href='https://www.youtube.com/channel/UCOCTIJiEVbSQaXeaScId_cQ/videos',
            href_title='https://www.youtube.com/channel/UCOCTIJiEVbSQaXeaScId_cQ/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Астамуринг',
            title_full='Астамуринг',
            href='https://www.youtube.com/channel/UCwqpU4SDWcRpL9YIuwYtF1A/videos',
            href_title='https://www.youtube.com/channel/UCwqpU4SDWcRpL9YIuwYtF1A/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Интервьюер',
            title_full='Зе Интервьюер',
            href='https://www.youtube.com/channel/UCuWDlf53jjxti-aUA4tBdsA/videos',
            href_title='https://www.youtube.com/channel/UCuWDlf53jjxti-aUA4tBdsA/videos',
            emojis='',
            inIndex=True
        ),
        # : {'title_full': ,'href': },
        feed(
            title='Банкир',
            title_full='Бегущий Банкир',
            href='https://www.youtube.com/channel/UCqVKtuYmKkVPaBeNFWRxlMw/videos',
            href_title='https://www.youtube.com/channel/UCqVKtuYmKkVPaBeNFWRxlMw/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Навальный',
            title_full='Алексей Навальный',
            href='https://www.youtube.com/channel/UCsAw3WynQJMm7tMy093y37A/videos',
            href_title='https://www.youtube.com/channel/UCsAw3WynQJMm7tMy093y37A/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Rapha',
            title_full='Rapha Films',
            href='https://www.youtube.com/channel/UCXYXxfVjxMppZY64-5baOsw/videos',
            href_title='https://www.youtube.com/channel/UCXYXxfVjxMppZY64-5baOsw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='MarkFood',
            title_full='Mark Wiens - Hungry tourist',
            href='https://www.youtube.com/channel/UCyEd6QBSgat5kkC6svyjudA/videos',
            href_title='https://www.youtube.com/channel/UCyEd6QBSgat5kkC6svyjudA/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Kaufman',
            title_full='Ron Kaufman',
            href='https://www.youtube.com/channel/UCGczcywiY2efmZ4lYb6jB9Q/videos',
            href_title='https://www.youtube.com/channel/UCGczcywiY2efmZ4lYb6jB9Q/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='FCade',
            title_full='Francis Cade',
            href='https://www.youtube.com/channel/UCHyBWpfAggsFPDc5A7l_eWA/videos',
            href_title='https://www.youtube.com/channel/UCHyBWpfAggsFPDc5A7l_eWA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Raquel',
            title_full='Raquel Reed',
            href='https://www.youtube.com/channel/UCcSow8gRPkLK0u-1pLMkZsw/videos',
            href_title='https://www.youtube.com/channel/UCcSow8gRPkLK0u-1pLMkZsw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='NurkFPV',
            title_full='Nurk FPV',
            href='https://www.youtube.com/channel/UCPCc4i_lIw-fW9oBXh6yTnw/videos',
            href_title='https://www.youtube.com/channel/UCPCc4i_lIw-fW9oBXh6yTnw/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='PostMortem',
            title_full='Post-Mortem Photography',
            href='https://www.youtube.com/channel/UCDFiX8wnIQwbAcnRlwSOowA/videos',
            href_title='https://www.youtube.com/channel/UCDFiX8wnIQwbAcnRlwSOowA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='VergeYT',
            title_full='The Verge (YouTube)',
            href='https://www.youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ/videos',
            href_title='https://www.youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='mono',
            title_full='monobank',
            href='https://www.youtube.com/channel/UClF9NLW6p4QZ28rGp8ExbAg/videos',
            href_title='https://www.youtube.com/channel/UClF9NLW6p4QZ28rGp8ExbAg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Yakushev',
            title_full='Andrei Yakushev',
            href='https://www.youtube.com/channel/UCfA7eqgBGvJuBcMS8PDFjcg/videos',
            href_title='https://www.youtube.com/channel/UCfA7eqgBGvJuBcMS8PDFjcg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title="ПланетаКино",
            title_full="Планета Кино",
            href='https://www.youtube.com/channel/UCrR7GJSvz481CxHQn-yXHJw/videos',
            href_title='https://www.youtube.com/channel/UCrR7GJSvz481CxHQn-yXHJw/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title="MLewin",
            title_full="Michelle Lewin",
            href="https://www.youtube.com/channel/UCXOF8RQ_v52K1uq6m_rMy1w/videos",
            href_title="https://www.youtube.com/channel/UCXOF8RQ_v52K1uq6m_rMy1w/videos",
            emojis='',
            inIndex=True
        ),
        feed(
            title="AdventureTeam",
            title_full="Adventure Team",
            href="https://www.youtube.com/channel/UCnusq0cEepVKVAlftFn8u5Q/videos",
            href_title="https://www.youtube.com/channel/UCnusq0cEepVKVAlftFn8u5Q/videos",
            emojis='',
            inIndex=True
        ),
        feed(
            title="OverwatchRU",
            title_full="Overwatch RU",
            href="https://www.youtube.com/channel/UCpW84gDcZu8wNQ-tUO5qE6A/videos",
            href_title="https://www.youtube.com/channel/UCpW84gDcZu8wNQ-tUO5qE6A/videos",
            emojis='',
            inIndex=True
        ),
        feed(
            title="cherrycrush",
            title_full="My Cherry Crush",
            href="https://www.youtube.com/channel/UC4lkVwG5XViZuoRrjdUqEeA/videos",
            href_title="https://www.youtube.com/channel/UC4lkVwG5XViZuoRrjdUqEeA/videos",
            emojis='',
            inIndex=False
        ),
        feed(
            title="Cosplay03",
            title_full="Milligan Vick",
            href="https://www.youtube.com/channel/UCPi1NLlECKm4VGpNjDUiBmg/videos",
            href_title="https://www.youtube.com/channel/UCPi1NLlECKm4VGpNjDUiBmg/videos",
            emojis='',
            inIndex=True
        ),
        feed(
            title="Snazzy",
            title_full="Snazzy Labs",
            href="https://www.youtube.com/channel/UCO2x-p9gg9TLKneXlibGR7w/videos",
            href_title="https://www.youtube.com/channel/UCO2x-p9gg9TLKneXlibGR7w/videos",
            emojis='',
            inIndex=True
        ),
        feed(
            title='Хач',
            title_full='ДНЕВНИК ХАЧА',
            href='https://www.youtube.com/channel/UCnbxcA3kZ_uUYIBHNvxpDQw/videos',
            href_title='https://www.youtube.com/channel/UCnbxcA3kZ_uUYIBHNvxpDQw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='ЧумацкийВелопробег',
            title_full='Чумацкий путь в Америку - велопробег',
            href='https://www.youtube.com/channel/UC4d-CwWxC8i96D9mKAAtnbA/videos',
            href_title='https://www.youtube.com/channel/UC4d-CwWxC8i96D9mKAAtnbA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Шелягина',
            title_full='Наташа Шелягина',
            href='https://www.youtube.com/channel/UC97y3hRp4lfOhAZpuSbYruQ/videos',
            href_title='https://www.youtube.com/channel/UC97y3hRp4lfOhAZpuSbYruQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='GMBNTech',
            title_full='GMBN Tech',
            href='https://www.youtube.com/channel/UC6juisijUAHcJLt23nk-qOQ/videos',
            href_title='https://www.youtube.com/channel/UC6juisijUAHcJLt23nk-qOQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='GMBN',
            title_full='GMBN',
            href='https://www.youtube.com/channel/UC_A--fhX5gea0i4UtpD99Gg/videos',
            href_title='https://www.youtube.com/channel/UC_A--fhX5gea0i4UtpD99Gg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='ArhyBES',
            title_full='ArhyBES',
            href='https://www.youtube.com/channel/UCby5ZKyxiSW3dz_Kg5VDU9w/videos',
            href_title='https://www.youtube.com/channel/UCby5ZKyxiSW3dz_Kg5VDU9w/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Blackpack',
            title_full='Blackpack',
            href='https://www.youtube.com/channel/UChXHexCL-d0538NwLClRDJQ/videos',
            href_title='https://www.youtube.com/channel/UChXHexCL-d0538NwLClRDJQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Сыендук',
            title_full='Сыендук',
            href='https://www.youtube.com/channel/UC-b89a0Fw6pNoP-g-_qLeiw/videos',
            href_title='https://www.youtube.com/channel/UC-b89a0Fw6pNoP-g-_qLeiw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Veddro',
            title_full='Veddro.com',
            href='https://www.youtube.com/channel/UCItSim1k6hOHyogg1LJ0JCQ/videos',
            href_title='https://www.youtube.com/channel/UCItSim1k6hOHyogg1LJ0JCQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Ленинград',
            title_full='Ленинград',
            href='https://www.youtube.com/channel/UCY0C6A3t3RTUN3BB65rWAgQ/videos',
            href_title='https://www.youtube.com/channel/UCY0C6A3t3RTUN3BB65rWAgQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='BadComedian',
            title_full='[BadComedian]',
            href='https://www.youtube.com/channel/UC6cqazSR6CnVMClY0bJI0Lg/videos',
            href_title='https://www.youtube.com/channel/UC6cqazSR6CnVMClY0bJI0Lg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='MKBHD',
            title_full='Marques Brownlee',
            href='https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ/videos',
            href_title='https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Corridor',
            title_full='Corridor Digital',
            href='https://www.youtube.com/channel/UCsn6cjffsvyOZCZxvGoJxGg/videos',
            href_title='https://www.youtube.com/channel/UCsn6cjffsvyOZCZxvGoJxGg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='KymNonStop',
            title_full='KymNonStop',
            href='https://www.youtube.com/channel/UCM6cd0hPii_FJOzZaxqGj7w/videos',
            href_title='https://www.youtube.com/channel/UCM6cd0hPii_FJOzZaxqGj7w/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='devinsupertramp',
            title_full='devinsupertramp',
            href='https://www.youtube.com/channel/UCwgURKfUA7e0Z7_qE3TvBFQ/videos',
            href_title='https://www.youtube.com/channel/UCwgURKfUA7e0Z7_qE3TvBFQ/videos',
            emojis='',
            inIndex=False
        ),
        feed(
            title='IFHT',
            title_full='IFHT Films',
            href='https://www.youtube.com/channel/UCTs59UCfP4YLUt6pDR_uLtg/videos',
            href_title='https://www.youtube.com/channel/UCTs59UCfP4YLUt6pDR_uLtg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Relaxation4K',
            title_full='4K Relaxation Channel',
            href='https://www.youtube.com/channel/UCg72Hd6UZAgPBAUZplnmPMQ/videos',
            href_title='https://www.youtube.com/channel/UCg72Hd6UZAgPBAUZplnmPMQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='LazySquare',
            title_full='Lazy Square',
            href='https://www.youtube.com/channel/UCZTc2bbF64cj_r0btHgaakw/videos',
            href_title='https://www.youtube.com/channel/UCZTc2bbF64cj_r0btHgaakw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Zaddrot',
            title_full='Zaddrot',
            href='https://www.youtube.com/channel/UCjQb9npdMq_u1rRBgoQ24fg/videos',
            href_title='https://www.youtube.com/channel/UCjQb9npdMq_u1rRBgoQ24fg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Notordinarytravel',
            title_full='Get out from the ordinary travel',
            href='https://www.youtube.com/channel/UCY5X52SAYFz3nejVwvjf9gg/videos',
            href_title='https://www.youtube.com/channel/UCY5X52SAYFz3nejVwvjf9gg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Gonzossm',
            title_full='Gonzossm',
            href='https://www.youtube.com/channel/UCoFEvb-8o_ONb8pFlZkz64g/videos',
            href_title='https://www.youtube.com/channel/UCoFEvb-8o_ONb8pFlZkz64g/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Apple',
            title_full='Apple',
            href='https://www.youtube.com/channel/UCE_M8A5yxnLfW0KghEeajjw/videos',
            href_title='https://www.youtube.com/channel/UCE_M8A5yxnLfW0KghEeajjw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Dobryak',
            title_full='Dobryak animations',
            href='https://www.youtube.com/channel/UCIQ1PyEVzV2sc4CXHKH2cSg/videos',
            href_title='https://www.youtube.com/channel/UCIQ1PyEVzV2sc4CXHKH2cSg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='CP',
            title_full='Cycling Pulse',
            href='https://www.youtube.com/channel/UCFtOJh5aZ2hqGA4wJnUEnZw/videos',
            href_title='https://www.youtube.com/channel/UCFtOJh5aZ2hqGA4wJnUEnZw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Поперечный',
            title_full='Данила Поперечный',
            href='https://www.youtube.com/channel/UCR-Hcwi27-Ee6VnGzmxE1pA/videos',
            href_title='https://www.youtube.com/channel/UCR-Hcwi27-Ee6VnGzmxE1pA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='RVerin',
            title_full='Ruslan Verin — Велопутешествия',
            href='https://www.youtube.com/channel/UCNttYYf1q2RVWkc0Rhulmdw/videos',
            href_title='https://www.youtube.com/channel/UCNttYYf1q2RVWkc0Rhulmdw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Storytelling',
            title_full='Hello Future Me (Storytelling)',
            href='https://www.youtube.com/channel/UCFQMO-YL87u-6Rt8hIVsRjA/videos',
            href_title='https://www.youtube.com/channel/UCFQMO-YL87u-6Rt8hIVsRjA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='SethHacks',
            title_full="Seth's Bike Hacks",
            href='https://www.youtube.com/channel/UCu8YylsPiu9XfaQC74Hr_Gw/videos',
            href_title='https://www.youtube.com/channel/UCu8YylsPiu9XfaQC74Hr_Gw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='SuperFun',
            title_full='Channel Super Fun',
            href='https://www.youtube.com/channel/UCBZiUUYeLfS5rIj4TQvgSvA/videos',
            href_title='https://www.youtube.com/channel/UCBZiUUYeLfS5rIj4TQvgSvA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='BlackDesertYT',
            title_full='Black Desert (YouTube)',
            href='https://www.youtube.com/channel/UCPzNpbcvaTtt-RtbESad1Jw/videos',
            href_title='https://www.youtube.com/channel/UCPzNpbcvaTtt-RtbESad1Jw/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='JYoung',
            title_full='Jonathan Young',
            href='https://www.youtube.com/channel/UC40gs0opj389ohjLnJIAJzA/videos',
            href_title='https://www.youtube.com/channel/UC40gs0opj389ohjLnJIAJzA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='VergeScience',
            title_full='Verge Science',
            href='https://www.youtube.com/channel/UCtxJFU9DgUhfr2J2bveCHkQ/videos',
            href_title='https://www.youtube.com/channel/UCtxJFU9DgUhfr2J2bveCHkQ/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Vox',
            title_full='Vox',
            href='https://www.youtube.com/channel/UCLXo7UDZvByw2ixzpQCufnA/videos',
            href_title='https://www.youtube.com/channel/UCLXo7UDZvByw2ixzpQCufnA/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Racked',
            title_full='Racked',
            href='https://www.youtube.com/channel/UC9HaoyVhTWca7s5QdjY91_A/videos',
            href_title='https://www.youtube.com/channel/UC9HaoyVhTWca7s5QdjY91_A/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='JYoung',
            title_full='Jonathan Young',
            href='https://www.youtube.com/channel/UCT4WspI1gXguL9kCOirYBBg/videos',
            href_title='https://www.youtube.com/channel/UCT4WspI1gXguL9kCOirYBBg/videos',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Anidub',
            title_full='Anidub Online',
            href='feed:https://online.anidub.com/rss.xml',
            href_title='feed:https://online.anidub.com/rss.xml',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Gam3',
            title_full='The Gam3',
            href='feed:https://thegam3.com/feed/',
            href_title='feed:https://thegam3.com/feed/',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Jago',
            title_full='Jagodibuja',
            href='feed://www.jagodibuja.com/feed/',
            href_title='feed://www.jagodibuja.com/feed/',
            emojis='',
            inIndex=True
        ),
        feed(
            title='vas3k',
            title_full='vas3k.ru',
            href='feed:https://vas3k.ru/rss/',
            href_title='https://vas3k.ru/',
            emojis='',
            inIndex=True
        ),
        feed(
            title='DisgustingMen',
            title_full='Disgusting Men',
            href='feed:https://disgustingmen.com/feed/',
            href_title='https://disgustingmen.com/',
            emojis='',
            inIndex=True
        ),
        feed(
            title='XKCD',
            title_full='XKCD',
            href='https://xkcd.com/rss.xml',
            href_title='https://xkcd.com/rss.xml',
            emojis='',
            inIndex=True
        ),
        feed(
            title='ReflectiveDesire',
            title_full='Reflective Desire',
            href='http://reflectivedesire.com/rss/',
            href_title='http://reflectivedesire.com/',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Verge',
            title_full='The Verge',
            href='https://www.theverge.com/rss/index.xml',
            href_title='https://www.theverge.com/',
            emojis='',
            inIndex=False
        ),
        feed(
            title='КабМин',
            title_full='Кабинет Министров Украины',
            href='https://www.kmu.gov.ua/api/rss',
            href_title='https://www.kmu.gov.ua/',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Shadman',
            title_full='Shadbase by Shadman',
            href='feed://www.shadbase.com/feed/',
            href_title='http://www.shadbase.com/',
            emojis='',
            inIndex=True
        ),
        feed(
            title='FisheyePlacebo',
            title_full='Fisheye Placebo',
            href='feed://readmanga.me/rss/manga?name=fisheye_placebo',
            href_title='http://readmanga.me/fisheye_placebo',
            emojis='',
            inIndex=True
        ),
        feed(
            title='OnePunchMan',
            title_full='One Punch Man',
            href='feed://readmanga.me/rss/manga?name=one_punch_man',
            href_title='http://readmanga.me/one_punch_man__A1be6f8',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Пик',
            title_full='Пик боевых искусств',
            href='feed://readmanga.me/rss/manga?name=martial_peak',
            href_title='http://readmanga.me/martial_peak',
            emojis='',
            inIndex=True
        ),
        feed(
            title='ТронБога',
            title_full='Трон, отмеченный Богом',
            href='feed://readmanga.me/rss/manga?name=shen_yin_wang_zuo',
            href_title='http://readmanga.me/shen_yin_wang_zuo',
            emojis='',
            inIndex=True
        ),
        feed(
            title='FairyTail100',
            title_full='Fairy Tail: 100 Years Quest',
            href='feed://readmanga.me/rss/manga?name=fairy_tail__100_years_quest',
            href_title='http://readmanga.me/fairy_tail__100_years_quest',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Brahmanden',
            title_full='Brahmanden: из Одессы с морковью',
            href='feed:https://feedfry.com/rss/11e89abaf37078f4a2c4a1e044ba7a50',
            # RSS is generated at https://feedfry.com/
            # test a bit as dates are not correct
            href_title='https://pikabu.ru/profile/Brahmanden',
            emojis='',
            inIndex=True
        ),
        feed(
            title='Yummyanime',
            title_full='Yummyanime',
            href='feed:https://twitrss.me/twitter_user_to_rss/?user=Yummyanime',
            href_title='https://yummyanime.com/anime-updates',
            emojis='',
            inIndex=False
        ),
        feed(
            title='BlackDesertTwi',
            title_full='BlackDesert (Twitter)',
            href='feed:https://twitrss.me/twitter_user_to_rss/?user=BlackDesertRU',
            href_title='https://gamenet.ru/games/blackdesert/news/',
            emojis='',
            inIndex=False
        ),
        feed(
            title='JoshuaWright',
            title_full='Joshua Wright (SlackWyrm)',
            href='feed://www.joshuawright.net/rss_joshuawright.xml',
            href_title='http://www.joshuawright.net/index.html',
            emojis='',
            inIndex=True
        ),
        feed(
            title='DTF',
            title_full='DTF (Everything new)',
            href='https://dtf.ru/rss/new',
            href_title='https://dtf.ru/top/month',
            emojis='',
            inIndex=False
        ),
        feed(
            title='Т——Ж',
            title_full='Тинькофф-Журнал',
            href='feed:https://journal.tinkoff.ru/feed/',
            href_title='https://journal.tinkoff.ru',
            emojis='',
            inIndex=True
        ),
        feed(
            title='shencomix',
            title_full='shencomix',
            href='http://shencomix.com/rss',
            href_title='http://shencomix.com/search/COMIC',
            emojis='',
            inIndex=True
        ),
        feed(
            title='octokuro',
            title_full='OCTOKURO',
            href='feed:https://www.octokuro.com/gallery?format=feed&type=rss',
            href_title='feed:https://www.octokuro.com/gallery',
            emojis='',
            inIndex=True
        ),
    ]


class feedUpdate(models.Model):
    class Meta:
        ordering = ['-datetime']
    name = models.CharField(max_length=140)
    href = models.CharField(max_length=420)
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
                result.extend(feedUpdate.list(item, feed.find(item).href))
            except KeyError:
                result.append(feedUpdate(
                    name="not found in feeds",
                    href="#",
                    datetime=datetime.now()+timedelta(hours=-3),
                    title=item))
                print("item: not found in feeds")

        return result

    def list(feedName, href):
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

            result = feedUpdate.list(feedName, href)

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
            feed = feedparser.parse(href)

            for item in feed["items"]:
                try:
                    dateresult = datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S %z')
                except ValueError:
                    if item["published"][-3] == ':':  # YouTube / TheVerge
                        dateresult = datetime.strptime(item["published"][:-3] + item["published"][-2:], '%Y-%m-%dT%H:%M:%S%z')
                    else:
                        try:  # except ValueError: # it is for webtooms import feeds['Gamer']
                            dateresult = datetime.strptime(item["published"], '%A, %d %b %Y %H:%M:%S %Z')  # +timedelta(hours=3)
                        except ValueError: # it is for pikabu Brahmanden import feeds['Brahmanden']
                            dateresult = datetime.strptime(item["published"], '%a, %d %b %Y %H:%M:%S %Z')  # .astimezone(timezone('UTC'))  # +timedelta(hours=3)

                toAdd = feedUpdate(
                    name=item["title_detail"]["value"],
                    href=item["links"][0]["href"],
                    datetime=dateresult,
                    title=feedName)
                result.append(toAdd)

        return result
