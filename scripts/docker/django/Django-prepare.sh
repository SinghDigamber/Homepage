#!/bin/sh

# python3 installation
apt-get install -y python3 python3-pip

# Homepage
python3 -m pip install django  # django
apt install -y libpq-dev python3-dev && python3 -m pip install psycopg2  # PostgreSQL

# Homepage/feedUpdate
python3 -m pip install requests  # downloads html code
python3 -m pip install beautifulsoup4  # used to parse html
python3 -m pip install collective.soupstrainer  # allows to parse part of the page
python3 -m pip install feedparser  # rss parser
python3 -m pip install python-dateutil  # universally parsing dates
python3 -m pip install tqdm  # progressbar for caching scripts

# Homepage/calenda
python3 -m pip install icalendar  # calendars
python3 -m pip install django_ical