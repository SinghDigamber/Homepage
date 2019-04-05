from django.conf.urls import url
from . import views

app_name = "weatherCast"
urlpatterns = [
    url(r'^$', views.weatherCastView.as_view(), name="index"),
]
