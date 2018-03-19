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

cp server-django.sh /etc/init.d/server-django.sh
cp server-django.sh /etc/init.d/server-django-cacher.sh
sudo chmod ugo+x /etc/init.d/server-django.sh
sudo chmod ugo+x /etc/init.d/server-django-cacher.sh

update-rc.d server-django.sh defaults
update-rc.d server-django-cache.sh defaults
# update-rc.d -f server-django.sh remove
# update-rc.d -f server-django-cache.sh remove

# sudo nano /etc/init.d/olehkrupko.com.django
# sudo nano /etc/init.d/olehkrupko.com.django-cacher
# sudo chmod ugo+x /etc/init.d/olehkrupko.com.django
# sudo chmod ugo+x /etc/init.d/olehkrupko.com.django-cacher
# update-rc.d -f olehkrupko.com.django remove
# update-rc.d -f olehkrupko.com.django-cacher remove

# ps auxw | grep runserver