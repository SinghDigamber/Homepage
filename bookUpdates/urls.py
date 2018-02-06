from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^System', views.IndexSystemView.as_view()),
    url(r'^Sculptor', views.IndexSculptorView.as_view()),

]
