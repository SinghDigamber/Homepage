"""Homepage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    # default
    url(r'^admin/', admin.site.urls),

    # main
    url(r'^', include('feedUpdate.urls', namespace="dashboard")),
    url(r'^feedUpdate/', include('feedUpdate.urls',
        namespace="feedUpdate")),

    # custom
    url(r'^university_TItaP/', include('university_TItaP.urls',
        namespace="university_TItaP")),

    # permanent
    url(r'^trakt/$', RedirectView.as_view(url='https://trakt.tv/users/olehkrupko/progress/watched/activity',
        permanent=True), name="Trakt"),
    url(r'^trakt/$', RedirectView.as_view(url='https://github.com/OlehKrupko/Homepage',
        permanent=True), name="GitHub"),
]
