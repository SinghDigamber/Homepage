from .models import event, calendar
from django.views.generic import ListView
from django_ical.views import ICalFeed
from datetime import datetime, date, timedelta
from icalendar import Calendar, Event


class eventListView(ListView):
    model = event
    template_name = "calenda/eventList.html"
    context_object_name = "fromView"

    def get_queryset(self):
        event_list = {}

        # today
        event_list['today'] = event.objects.filter(start__date=date.today(), end__gte=datetime.now())

        # tomorrow
        event_list['tomorrow'] = event.objects.filter(start__date=date.today() + timedelta(days=1))

        # until end of the week
        after_tomorrow = date.today() + timedelta(days=2)

        days_ahead = 6 - date.today().weekday()  # 0 = Monday, 1=Tuesday, 2=Wednesday...
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        sunday = date.today() + timedelta(days=days_ahead)

        event_list['this_week'] = event.objects.filter(start__date__gt=after_tomorrow, end__date__lte=sunday)

        return {
            'page_title': "cписок",
            # 'event_list': event_list[:items_limit],
            'event_list': event_list,
        }


class icsView(ICalFeed):
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'

    def items(self):
        return event.objects.all()

    def item_title(self, item):
        return item.calendar+": "+item.title

    def item_description(self, item):
        return "["+item.calendar+"] - "+item.title

    def item_link(self, item):
        if item.href != None:
            return item.href
        else:
            return "/calenda/"

    def item_start_datetime(self, item):
        return item.start

    def item_end_datetime(self, item):
        return item.end

    def item_organizer(self, item):
        return item.calendar
