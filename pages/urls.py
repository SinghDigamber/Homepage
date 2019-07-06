from django.conf.urls import url
from . import views

app_name = "pages"
urlpatterns = [
    url(r'^page/(?P<file_name>([0-9|a-z|A-Z|_|.])*)$', views.pageView.as_view(), name="page"),

    url(r'^$', views.pageIndexView.as_view(), name="index"),
]