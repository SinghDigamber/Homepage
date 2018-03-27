from django.conf.urls import url
from django.urls import path
from . import views

app_name = "university_TItaP"
urlpatterns = [
    url(r'^$', views.university_TItaPIndexView.as_view(), name="index"),
]
