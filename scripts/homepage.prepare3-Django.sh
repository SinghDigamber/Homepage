#!/bin/sh

# python installations
sudo python3 -m pip install django  # django
sudo python3 -m pip install requests  # downloads html
sudo python3 -m pip install beautifulsoup4  # used to parse html
sudo python3 -m pip install collective.soupstrainer  # allows to parse part of the page
sudo python3 -m pip install feedparser  # rss parser
sudo python3 -m pip install python-dateutil  # universally parsing dates
sudo python3 -m pip install tqdm  # progressbar for caching scripts
sudo python3 -m pip install icalendar  # calendars
sudo python3 -m pip install psycopg2  # PostgreSQL 
sudo python3 -m pip install django_ical

# system set up
sudo rm -rf /home/pi/Projects/Homepage
git clone https://github.com/OlehKrupko/Homepage /home/pi/Projects/Homepage
