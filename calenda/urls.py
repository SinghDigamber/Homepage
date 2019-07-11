from django.conf.urls import url
from . import views

app_name = "calenda"
urlpatterns = [
    url(r'^$', views.eventListView.as_view(), name="list"),
    url(r'^ics$', views.icsView.as_view(), name="ics"),
]
