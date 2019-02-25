from django.conf.urls import url
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^(?P<mode>(|index|force))$', views.feedUpdateIndexView.as_view(), name="index"),  # main fU feed with modes
    url(r'^(?P<feeds>([0-9|а-я|А-Я|a-z|A-Z|_|+|—])*)/(?P<mode>(|index|force))?$',
        views.feedUpdateIndexView.as_view(), name="feed"),  # view separate feeds
    url(r'^feeds$', views.feedIndexView.as_view(), name="feeds"),  # list feeds
]
