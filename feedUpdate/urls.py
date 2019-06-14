from django.conf.urls import url
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^tests$', views.feedTestsView.as_view(), name="tests"),

    url(r'^feeds$', views.feedIndexView.as_view(), name="feeds"),  # list feeds
    url(r'^feedsAll$', views.feedIndexFullView.as_view(), name="feedsAll"),  # list all feeds
    url(r'^myActivity/(?P<mode>(|index|force))', views.myActivityView.as_view(), name="myActivity"),  # list feeds

    url(r'^(?P<mode>(|index|force))$', views.feedUpdateIndexView.as_view(), name="index"),  # main fU feed with modes
    url(r'^(?P<feeds>([0-9|а-я|ё|А-Я|Ё|a-z|A-Z|_|+|—])*)/(?P<mode>(|index|force))?$',
        views.feedUpdateIndexView.as_view(), name="feed"),  # view separate feeds with filters
]
