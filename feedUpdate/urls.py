from django.conf.urls import url
from django.urls import path
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^$', views.feedUpdateIndexView.as_view(), name="index"),
    url(r'^more', views.feedUpdateIndexMoreView.as_view(), name="index/all"),
    url(r'^force$', views.feedUpdateForceIndexView.as_view(), name="index/force"),
    url(r'^(?P<feeds>([0-9|а-я|А-Я|a-z|A-Z|_|+])+)$', views.feedUpdateIndexView.as_view(), name="feed"),
    url(r'^(?P<feeds>([0-9|а-я|А-Я|a-z|A-Z|_|+])+)/force$', views.feedUpdateForceIndexView.as_view(), name="feed/force"),
]
