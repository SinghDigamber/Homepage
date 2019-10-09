from django.conf.urls import url
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^$', views.feedUpdateIndexView.as_view(), name="main"),  # main fU feed with modes
    url(r'^index:(?P<mode>(index|force|more))$', views.feedUpdateIndexView.as_view(), name="index"),  # main fU feed with modes
    url(r'^other:(?P<mode>(index|force|more))', views.otherView.as_view(), name="other"),  # list other

    # pages
    url(r'^feeds$', views.feedIndexView.as_view(), name="feeds"),  # list feeds
    url(r'^feedsAll$', views.feedIndexFullView.as_view(), name="feedsAll"),  # list all feeds
    url(r'^tests$', views.feedTestsView.as_view(), name="tests"),
    url(r'^rss$', views.feedUpdateFeed(), name="rss"),
    
    url(r'^custom?feeds=(?P<feeds>([0-9|а-я|ё|А-Я|Ё|a-z|A-Z|_|+|—])*)/(?P<mode>(|index|force|more))?$',
        views.feedUpdateIndexView.as_view(), name="feed"),  # view separate feeds with filters
]
