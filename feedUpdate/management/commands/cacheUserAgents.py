from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import requests
import os
from .models import keyValue

class Command(BaseCommand):
    help = 'downloads a BIG list of user agents'

    def add_arguments(self, parser):
        parser.add_argument('--backup', action='store_true')
        parser.add_argument('--logLength', action='store_true')

    def handle(self, *args, **options):
        soup = requests.get('http://useragentstring.com/pages/useragentstring.php?name=All')
        soup = BeautifulSoup(soup.text, "html.parser")
        
        UserAgent_path = os.path.join("static", "feedUpdate")
        if options['backup']:
            UserAgent_path = os.path.join(UserAgent_path, "user-agents.txt")
        else:
            UserAgent_path = os.path.join(UserAgent_path, "user-agents-backup.txt")
        os.remove(UserAgent_path)
        open(UserAgent_path, 'a').close()

        UserAgent_list = []
        for each in soup.find_all('li'):
            UserAgent_list.append(each.find('a').getText())

        if options['logLength']:
            lines = 0
        with open(UserAgent_path, 'a') as UserAgent_file:
            for each in UserAgent_list:
                UserAgent_file.write(each+'\n')
                lines += 1

        if options['logLength']:
            keyValue.objects.filter(key='weatherNowSum')[0].value
