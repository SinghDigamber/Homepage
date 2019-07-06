#!/bin/sh

ssh pi@krupko.space -p 8022
sudo raspi-config

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
sudo python3 -m pip install python-dateutil  # universally parsing dates
sudo python3 -m pip install tqdm  # progressbar for caching scripts
sudo python3 -m pip install icalendar

sudo rm -rf /home/pi/Projects/Homepage
cd ~
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



python3 manage.py makemigrations
python3 manage.py migrate


ports used:
80 >> pi 80 (web server)
8080 >> mac 8080 (test web server)
8022 >> pi 22 (ssh)
8033 >> pi 3306

sudo nano ~/.config/lxsession/LXDE-pi/autostart
# add:
@unclutter -idle 0.1
@chromium-browser --kiosk --noerrdialogs --profile=Default --app=https://youtube.com/tv

sudo apt update
sudo apt install postgresql

sudo systemctl status postgresql

sudo -i -u postgres
psql

sudo nano /etc/postgresql/9.4/main/pg_hba.conf
# Add the following line to the configuration file:
host all all 192.168.1.200/24 trust
host all all 192.168.1.201/24 trust

sudo nano /etc/postgresql/9.4/main/postgresql.conf
# Find the following line
listen_addresses='localhost'
#Change it to
listen_addresses='*'

sudo systemctl restart postgresql

\password postgres

create user pi with password 'bali4dead';
alter role pi set client_encoding to 'utf8';
alter role pi set default_transaction_isolation to 'read committed';
alter role pi set timezone to 'UTC';
create database homepage_django owner pi;
\q

## PyCharm: install psycopg2-binary
sudo pip install django psycopg2-binary
python3 manage.py createsuperuser
