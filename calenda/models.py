from django.db import models
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import datetime
import dateutil.parser as datetimeparser
from datetime import timedelta, date
from icalendar import Calendar, Event


class event(models.Model):
    class Meta:
        ordering = ['start']
    title = models.CharField(max_length=42)
    description = models.CharField(max_length=420, null=True)
    calendar = models.CharField(max_length=42)

    href = models.CharField(max_length=420, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)


class calendar(models.Model):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=42)
    title_full = models.CharField(max_length=140)

    href = models.CharField(max_length=420)
    emojis = models.CharField(max_length=14, null=True)

    def calendars_from_file():
        from .calendars import calendars

        return calendars

    def parse(self):
        result = []

        if self.href.find('https://sportevent.com.ua/events/') != -1:
            soup = requests.get(self.href)
            soupStrainer = SoupStrainer('div', attrs={'class': 'leftside events'})
            soup = BeautifulSoup(soup.text, "html.parser", parse_only=soupStrainer)

            for li in soup.find_all('li'):
                result_title = li.find('div', attrs={'class': 'event-stext'})['title']
                result_description = li.find('div', attrs={'class': 'event-stext'}).getText()
                result_href = "https://sportevent.com.ua/"+li.find('div')['onclick'][15:-2]

                # datetime is too complicated:
                start_year = datetime.now().date().year

                start_month = li.find('div', attrs={'class': 'calendar event_date'})
                start_month = start_month.find('span', attrs={'class': 'month'}).getText()

                if start_month == "Июня":
                    start_month=6
                elif start_month == "Июля":
                    start_month=7
                elif start_month == "Августа":
                    start_month=8
                elif start_month == "Сентября":
                    start_month=9
                elif start_month == "Октября":
                    start_month=10
                elif start_month == "Ноября":
                    start_month=11
                elif start_month == "Декабря":
                    start_month=12
                else:
                    start_month=42

                start_day = li.find('div', attrs={'class': 'calendar event_date'})
                start_day = start_day.find('span', attrs={'class': 'day'}).getText()
                start_day = int(start_day)

                result_start = datetime(year=start_year, month=start_month, day=start_day)

                result_end = result_start + timedelta(0, 23*60*60+59*60+59)

                result.append(event(
                    title=result_title[:42],
                    description=result_description,
                    href=result_href,
                    start=result_start,
                    end=result_end,
                    calendar=self.title
                ))

        if self.href.find('https://prime-orchestra.com/en/tours/') != -1:
            soup = requests.get(self.href)
            soupStrainer = SoupStrainer('div', attrs={'class': 'event-list isogrid'})
            soup = BeautifulSoup(soup.text, "html.parser", parse_only=soupStrainer)

            for each in soup.find("div"):
                if str(each).find("grid-item event dark-event") == 12:
                    result_year = each["class"][-1][1:]
                    result_month = each.find('span', attrs={'class': 'event-month'}).getText()
                    result_day = each.find('span', attrs={'class': 'event-date'}).getText()
                    result_start = result_year +" "+ result_month +" "+ result_day
                    result_start = datetimeparser.parse(result_start)

                    result_end = result_start + timedelta(0, 23*60*60+59*60+59)

                    result_href = each.find('a', attrs={'class': 'the-button-wrapper the-button-wrapper-details'})['href']

                    result_location = each.find('span', attrs={'class': 'event-title'}).getText()
                    result_location = ' '.join(result_location.split())
                    result_title = each.find('small').getText()
                    result_title = ' '.join(result_title.split())
                    result_title = result_title +" - "+ result_location

                    result.append(event(
                        title=result_title[:42],
                        href=result_href,
                        start=result_start,
                        end=result_end,
                        calendar=self.title
                    ))

        if self.href.find('https://kharkov.internet-bilet.ua') != -1:
            soup = requests.get(self.href)
            soupStrainer = SoupStrainer('ul', attrs={'class': 'events-list-style'})
            soup = BeautifulSoup(soup.text, "html.parser", parse_only=soupStrainer)

            for li in soup.find_all('li'):
                #print(li)
                #print("\n\n----new----\n\n")

                result_title = li.find('img')['alt']
                result_city = li.find('span', attrs={'class': 'city'}).getText()
                result_place = li.find('span', attrs={'class': 'place'}).getText()
                result_title = result_title +', '+ result_city +', '+ result_place
                # print(result_title)

                result_href = li.find('a')['href']
                # print(result_href)

                result_start = li.find('meta', attrs={'itemprop': 'startDate'})['content']
                result_start = datetimeparser.parse(result_start)
                # print(result_start)

                result_end = result_start + timedelta(0, 2*60*60)

                result.append(event(
                    title=result_title[:42],
                    description=result_title,
                    href=result_href,
                    start=result_start,
                    end=result_end,
                    calendar=self.title
                ))

        if self.href.find('http://xtt.herokuapp.com/plan.ics') != -1:
            soup = requests.get(self.href)
            soup = BeautifulSoup(soup.text, "html.parser")
            soup = str(soup)

            for each_event in soup.split('END:VEVENT'):
                if each_event.find("DTSTART:") != -1:
                    #print(event)

                    result_start = each_event.find("DTSTART:")+len("DTSTART:")
                    result_start = each_event[result_start:]
                    result_start = result_start[:result_start.find("\n")]
                    result_start = datetimeparser.parse(result_start)
                    #print("start:", result_start)

                    result_end = each_event.find("DTEND:")+len("DTEND:")
                    result_end = each_event[result_end:]
                    result_end = result_end[:result_end.find("\n")]
                    result_end = datetimeparser.parse(result_end)
                    #print("end:", result_end)

                    result_title = each_event.find("SUMMARY:")+len("SUMMARY:")
                    result_title = each_event[result_title:]
                    result_title = result_title[:result_title.find("\n")]
                    #print("title:", result_title)

                    result_href = each_event.find("URL:")+len("URL:")
                    result_href = each_event[result_href:]
                    result_href = result_href[:result_href.find("\n")]
                    # print("href:", result_href)

                    # print("\n\n----new----\n\n")

                    result.append(event(
                        title=result_title[:42],
                        description=result_title,
                        href=result_href,
                        start=result_start,
                        end=result_end,
                        calendar=self.title
                    ))

        if self.href.find('webcal://') != -1:
            self.href = 'http://'+self.href[9:]
            soup = requests.get(self.href)
            soup = BeautifulSoup(soup.text, "html.parser")
            soup = str(soup)

            gcal = Calendar.from_ical(soup)
            for component in gcal.walk():
                if component.name == "VEVENT" and not component.get('RRULE', False):
                    result_title = component.get('summary')
                    result_description = component.get('description')
                    if result_description is not None:
                        result_description = result_description[:420]
                    result_href = component.get('href')
                    result_start = component.get('dtstart').dt
                    result_end = component.get('dtend').dt

                    result.append(event(
                        title=result_title[:42],
                        description=result_description,
                        href=result_href,
                        start=result_start,
                        end=result_end,
                        calendar=self.title
                    ))

        return result
