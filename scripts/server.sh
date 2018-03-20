#!/bin/sh

ssh pi@192.168.1.201
python3 -m pip install -U --force-reinstall pip
python3 -m pip install --upgrade pip
sudo python3 -m pip install django~=2.0.2

sudo python3 -m pip install requests # downloads html
sudo python3 -m pip install beautifulsoup4 # used to parse html
sudo python3 -m pip install collective.soupstrainer # allows to parse part of the page
sudo apt-get update
sudo apt-get -f install --fix-missing
sudo python3 -m pip install lxml # html parser
sudo apt-get install libxml2-dev libxslt1-dev # requied for lxml
sudo python3 -m pip install lxml # html parser
sudo python3 -m pip install feedparser # rss parser

cp ~/Projects/Homepage/scripts/homepage.* /etc/init.d/
# sudo chmod ugo+x /etc/init.d/server-django.sh
# sudo chmod ugo+x /etc/init.d/server-django-cacher.sh

update-rc.d com.olehkrupko.homepage defaults
update-rc.d com.olehkrupko.homepage.watcher.* defaults
# update-rc.d -f server-django.sh remove
# update-rc.d -f server-django-cache.sh remove

# ps auxw | grep runserver