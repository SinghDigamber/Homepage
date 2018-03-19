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

#!/bin/sh

### BEGIN INIT INFO
# Provides:          olehkrupko.com.django
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      1 0 6
# Short-Description: launches Django demon
### END INIT INFO

rm -rf /home/pi/Homepage
git clone https://github.com/OlehKrupko/Homepage /home/pi/Homepage
python3 /home/pi/Homepage/manage.py runserver 192.168.1.201:8000

#!/bin/sh

### BEGIN INIT INFO
# Provides:          olehkrupko.com.django-cacher
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      1 0 6
# Short-Description: launches Django-cacher demon
### END INIT INFO

while sleep 600; do curl "http://home.olehkrupko.com/bookUpdates/cache"; done

sudo nano /etc/init.d/olehkrupko.com.django
sudo nano /etc/init.d/olehkrupko.com.django-cacher

sudo chmod ugo+x /etc/init.d/olehkrupko.com.django
sudo chmod ugo+x /etc/init.d/olehkrupko.com.django-cacher

python3 ~/Homepage/manage.py migrate
python3 ~/Homepage/manage.py createsuperuser

ps auxw | grep runserver