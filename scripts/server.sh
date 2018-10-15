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

rm -rf /home/pi/Projects/Homepage
git clone https://github.com/OlehKrupko/Homepage /home/pi/Projects/Homepage

# sudo cp ~/Projects/Homepage/scripts/homepage.server /etc/init.d/
# sudo cp ~/Projects/Homepage/scripts/homepage.watcher /etc/init.d/
# sudo chmod ugo+x /etc/init.d/server-django.sh
# sudo chmod ugo+x /etc/init.d/server-django-cacher.sh


ps auxw | grep runserver

sudo cp /home/pi/Projects/Homepage/scripts/homepage.cacheUpdate.service /lib/systemd/system/homepage.cacheUpdate.service
sudo cp /home/pi/Projects/Homepage/scripts/homepage.cacheUpdate.timer /lib/systemd/system/homepage.cacheUpdate.timer
sudo cp /home/pi/Projects/Homepage/scripts/homepage.server.service /lib/systemd/system/homepage.server.service

nano /tmp/homepage.cacheUpdate.service.result


sudo systemctl status homepage.server.service
sudo systemctl enable homepage.server.service
sudo systemctl start homepage.server.service




sudo systemctl status homepage.cacheUpdate.service
sudo systemctl enable homepage.cacheUpdate.service
sudo systemctl start homepage.cacheUpdate.service



systemctl -all list-timers

sudo systemctl status

/opt/vc/bin/vcgencmd measure_temp
