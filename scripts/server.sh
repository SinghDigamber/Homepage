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

sudo cp ~/Projects/Homepage/scripts/homepage.* /etc/init.d/
# sudo chmod ugo+x /etc/init.d/server-django.sh
# sudo chmod ugo+x /etc/init.d/server-django-cacher.sh

sudo update-rc.d homepage.server defaults
sudo update-rc.d homepage.watcher defaults
# update-rc.d -f homepage.server remove
# update-rc.d -f homepage.watcher remove

ps auxw | grep runserver

sudo nano /lib/systemd/system/homepage.watcher.service

[Unit]
Description=Homepage cache updater

[Service]
ExecStart=/home/pi/Projects/Homepage/scripts/homepage.watcher

[Install]
WantedBy=multi-user.target

sudo systemctl status homepage.watcher.service
sudo systemctl enable homepage.watcher.service
sudo systemctl start homepage.watcher.service



sudo nano /lib/systemd/system/homepage.server.service

[Unit]
Description=Homepage server

[Service]
ExecStart=/home/pi/Projects/Homepage/scripts/homepage.server

[Install]
WantedBy=multi-user.target

sudo systemctl status homepage.server.service
sudo systemctl enable homepage.server.service
sudo systemctl start homepage.server.service