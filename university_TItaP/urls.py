from django.conf.urls import url
from django.urls import path
from . import views

app_name = "university_TItaP"
urlpatterns = [
    url(r'^$', views.university_TItaPIndexView.as_view(), name="index"),
    url(r'^vector/update/(?P<pk>[0-9]+)$', views.VectorUpdateView.as_view()),
    url(r'^vector/update/alternative/index/university_TItaP/vector/update/(?P<pk>[0-9]+)$', views.VectorIndexView.as_view()),
]
