from os.path import join
from os import remove
import requests

from django.core.management.base import BaseCommand, CommandError
from Dashboard.models import keyValue

from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'downloads a BIG list of user agents'

    def add_arguments(self, parser):
        parser.add_argument('--backup', action='store_true')
        parser.add_argument('--writeLength', action='store_true')

    def handle(self, *args, **options):
        request = requests.get('http://useragentstring.com/pages/useragentstring.php?name=All')
        request = BeautifulSoup(request.text, "html.parser")
        
        UserAgent_path = join("static", "feedUpdate")
        if options['backup']:
            UserAgent_path = join(UserAgent_path, "user-agents.txt")
        else:
            UserAgent_path = join(UserAgent_path, "user-agents-backup.txt")
        
        remove(UserAgent_path)  # delete old file version
        open(UserAgent_path, 'a').close()  # create empty file

        UserAgent_list = []
        for each in request.find_all('li'):
            UserAgent_list.append(each.find('a').getText())

        if options['writeLength']:
            lines = 0
        with open(UserAgent_path, 'a') as UserAgent_file:
            for each in UserAgent_list:
                UserAgent_file.write(each+'\n')

                if options['writeLength']:
                    lines += 1

        if options['writeLength']:
            object_list = keyValue.objects.filter(key='UserAgentLen')

            if len(object_list) > 0:
                if len(object_list) > 1:
                    object_list[1:].delete()

                UserAgentLen = object_list[0]
                UserAgentLen.value = lines
                UserAgentLen.save()
            else:
                UserAgentLen = keyValue(key='UserAgentLen', value=lines)
                UserAgentLen.save()
