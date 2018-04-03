from django.conf.urls import url
from django.urls import path
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^$', views.feedUpdateIndexView.as_view(), name="index"),
    url(r'^cache$', views.feedUpdateCacheView.as_view(), name="cache"),
    url(r'^force$', views.feedUpdateForceIndexView.as_view(), name="force"),
    url(r'^(?P<books>([0-9|а-я|А-Я|a-z|A-Z|+])+)$', views.feedUpdateIndexView.as_view(), name="book"),
    url(r'^(?P<books>([0-9|а-я|А-Я|a-z|A-Z|+])+)/force$', views.feedUpdateForceIndexView.as_view(), name="book/force"),
]
