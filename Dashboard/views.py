from django.views.generic import ListView
from .models import Dashboard


class DashboardView(ListView):
    model = Dashboard
    template_name = "Dashboard/main.html"
    context_object_name = "fromView"

    def get_queryset(self):
        Dashboard()
        return Dashboard