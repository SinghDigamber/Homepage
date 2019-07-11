from .models import page
from django.views.generic import ListView


class pageView(ListView):
    model = page
    template_name = "pages/page.html"
    context_object_name = "fromView"

    def get_queryset(self):
        return {
            'file_name': self.kwargs['file_name'],
        }


class pageIndexView(ListView):
    model = page
    template_name = "pages/pages.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        header = "Заметки"

        # calculations
        page_list = page.objects.all()

        # results
        return {
            'page': {
                'title': header,
            },
            'page_list': page_list,
        }
