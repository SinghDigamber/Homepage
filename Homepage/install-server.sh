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
cd ~
rm -rf ~/Homepage
git clone https://github.com/OlehKrupko/Homepage
python3 ~/Homepage/manage.py runserver 192.168.1.201:8000
cd ~

sudo nano /etc/init.d/olehkrupko.com.django
sudo chmod ugo+x /etc/init.d/olehkrupko.com.django

python3 ~/Homepage/manage.py migrate
python3 ~/Homepage/manage.py createsuperuser