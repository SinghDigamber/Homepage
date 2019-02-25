from django.conf.urls import url
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^$', views.feedUpdateIndexView.as_view(), name="index"),
    url(r'^feeds/$', views.feedIndexView.as_view(), name="feeds"),  # return list of feeds with links to them
    url(r'^(?P<feeds>([0-9|а-я|А-Я|a-z|A-Z|_|+|—])*)?(?P<mode>([/|a-z]){6})?$',
        views.feedUpdateIndexView.as_view(), name="feed"),
]
