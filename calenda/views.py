from .models import event, calendar
from django.views.generic import ListView
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


class icsView(ListView):
    model = event
    template_name = "calenda/calendar.ics"
    context_object_name = "fromView"

    def get_queryset(self):
        cal = Calendar()

        for each in event.objects.all():
            to_add = Event()
            to_add.add('summary', each.calendar+": "+each.title)
            to_add.add('dtstart', each.start)
            to_add.add('dtend', each.end)
            to_add.add('href', each.href)

            cal.add_component(to_add)

        result = cal.to_ical()

        return result
