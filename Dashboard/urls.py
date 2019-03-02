from django.conf.urls import url
from . import views

app_name = "Dashboard"
urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name="Dashboard"),
]
