from django.shortcuts import render
from .models import feedUpdate, feed
from django.views.generic import ListView
import socket
from django.shortcuts import redirect
from django.urls import reverse


class feedIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/feeds.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        header = "Ленты обновлений"

        # calculations
        feed_list = feed.objects.all()

        # results
        return {
            'title': header,
            'feed_list': feed_list,
        }


class myActivityView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        header = "Моя активность"
        multibook = True
        items_limit = 42

        # calculations
        title_list = []
        for each in feed.feeds_by_emoji('👤'):
            title_list.append(each.title)
        print(feedUpdate.objects.filter(title__in=title_list))

        feedUpdate_list = list(feedUpdate.objects.filter(title__in=title_list)[:items_limit])

        # results
        return {
            'title': header,
            'feedUpdate_list': feedUpdate_list,
            'multibook': multibook,
        }


class feedUpdateIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        items_limit = 42

        # calculations
        # multibook checker
        if not self.kwargs.get('feeds', False):
            multibook = True
        elif len(self.kwargs['feeds'].split("+")) > 1:
            multibook = True
        else:
            multibook = False
        print("multibook: " + str(multibook))

        # page_title generation
        page_title = "Обновления"
        if not multibook:
            feed_one = feed.find(self.kwargs['feeds'])
            if feed_one.title_full:
                page_title = feed_one.title_full
            else:
                page_title = feed_one.title
        elif self.kwargs.get('feeds', False):
            page_title = self.kwargs['feeds']
        print("page_title: " + str(page_title))

        # feedName generation for buttons
        try:
            feedName = self.kwargs['feeds']
        except KeyError:
            feedName = "Обновления"
        print("feedName: " + str(feedName))

        # feed_list generation
        feed_list = []
        if not multibook:
            feed_list.append(feed.find(feedName))
        elif not self.kwargs.get('feeds', False):
            feed_list = feed.feeds_by_emoji()
        else:
            feed_list = feedUpdate.objects.filter(title__in=page_title.split("+"))
        print("feed_list: " + str(feed_list))


        # get feedUpdate_list
        feedUpdate_list = []
        if self.kwargs.get('mode', False) == "index" or self.kwargs.get('mode', False) == "":
            if page_title == "Обновления":
                feed_titles = []
                for each in feed.feeds_by_emoji():
                    feed_titles.append(each.title)
                feedUpdate_list = list(feedUpdate.objects.filter(title__in=feed_titles)[:items_limit])
            else:
                feedUpdate_list = list(feedUpdate.objects.filter(title__in=self.kwargs['feeds'].split("+"))[:items_limit])
        elif self.kwargs['mode'] == "force":
            page_title += ": Forced"
            print(1, feedUpdate_list)
            for each in feed_list:
                for feedUpdate_item in feed.parse(each):
                    feedUpdate_list.append(feedUpdate_item)
            print(2, feedUpdate_list[0])
            feedUpdate_list.sort(key=lambda feedUpdate_list_item: str(feedUpdate_list_item.datetime), reverse=True)

        return {
            'page_title': page_title,
            'feedName': feedName,
            'feedUpdate_list': feedUpdate_list,
            'multibook': multibook,
        }
