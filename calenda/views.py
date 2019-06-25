from .models import event, calendar
from django.views.generic import ListView


class eventListView(ListView):
    model = event
    template_name = "calenda/eventList.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # items_limit = 4200

        event_list = event.objects.all()
        # today
        # this week
        # each month separately

        return {
            'page_title': "cписок",
            # 'event_list': event_list[:items_limit],
            'event_list': event_list,
        }
