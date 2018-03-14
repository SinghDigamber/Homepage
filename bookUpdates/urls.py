from django.conf.urls import url
from django.urls import path
from . import views

app_name="bookUpdates"
urlpatterns = [
    url(r'^$', views.BookIndexView.as_view(), name="index"),
    url('^(?P<books>([0-9|а-я|А-Я|a-z|A-Z|+])+)$', views.BookIndexView.as_view(), name="book"),

]
