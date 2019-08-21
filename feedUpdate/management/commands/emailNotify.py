from django.core.management.base import BaseCommand, CommandError
from feedUpdate.models import feedUpdate, feed
from datetime import date, time, timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'updates caches in DB'

    def add_arguments(self, parser):
        parser.add_argument('--fromYesterday', action='store_true')

    def handle(self, *args, **options):
        # constants
        email_from = 'feedUpdate@krupko.space'
        email_subject = 'Your regular feedUpdates are here'
        list_subscribers = {
            '📧': 'oleh.krupko@gmail.com',
        }

        # execution
        if options['fromYesterday']:
            date_yesterday = date.today() - timedelta(days=1)

            list_feedUpdate_fromYesterday = feedUpdate.objects.filter(datetime__date__gte=date_yesterday)
            
            for key, email in list_subscribers.items():
                list_feed_notify = list(feed.feeds_by_emoji(key))

                list_feed_titles = []
                for each in list_feed_notify:
                    list_feed_titles.append(each.title)
                
                list_feedUpdate_results = list_feedUpdate_fromYesterday.filter(title__in=list_feed_titles)
                list_feedUpdate_results = list(list_feedUpdate_results)

                html_content = render_to_string(
                    'feedUpdate/email.html', {
                        'fromView': {
                            'page_title': 'Обновления',
                            'feedName': 'Обновления',
                            'feedUpdate_list': list_feedUpdate_results,
                            'multibook': True,
                        }
                    }
                ) # render with dynamic value
                text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

                # create the email, and attach the HTML version as well.
                msg = EmailMultiAlternatives(email_subject, text_content, email_from, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                