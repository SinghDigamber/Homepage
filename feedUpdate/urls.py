from django.conf.urls import url
from django.urls import path
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^$', views.feedUpdateIndexView.as_view(), name="index"),
    url(r'^(?P<feeds>([0-9|а-я|А-Я|a-z|A-Z|_|+|—])*)(\/)?(?P<force>(\/force))?$',  # add limit option as well
    url(r'^feeds/$', views.feedIndexView.as_view(), name="feeds"),  # return list of feeds with links to them
        views.feedUpdateIndexView.as_view(), name="feed"),
]
