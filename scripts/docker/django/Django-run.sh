#!/bin/sh

# downloading code repository
apt-get install -y git
git clone https://github.com/OlehKrupko/Homepage /Homepage

# caching before launch
# python3 manage.py cacheFeedUpdate --parseFeeds --log;
# python3 manage.py cacheCalendars --parseCalendars;
# python3 manage.py cachePages --parsePages;
# python3 manage.py cacheUserAgents --logLength;

# launch web server # local launch # python3 manage.py runserver 192.168.1.200:8000
# run everything on server side?