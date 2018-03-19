from django.conf.urls import url
from django.urls import path
from . import views

app_name = "bookUpdate"
urlpatterns = [
    url(r'^$', views.bookUpdateIndexView.as_view(), name="index"),
    url(r'^cache$', views.bookUpdateCacheView.as_view(), name="cache"),
    url(r'^force$', views.bookUpdateForceIndexView.as_view(), name="force"),
    url(r'^(?P<books>([0-9|а-я|А-Я|a-z|A-Z|+])+)$', views.bookUpdateIndexView.as_view(), name="book"),
    url(r'^(?P<books>([0-9|а-я|А-Я|a-z|A-Z|+])+)/force$', views.bookUpdateForceIndexView.as_view(), name="book/force"),
]
