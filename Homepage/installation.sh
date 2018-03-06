ssh pi@192.168.1.201
python3 -m pip install -U --force-reinstall pip
python3 -m pip install --upgrade pip
sudo python3 -m pip install django~=2.0.2

sudo python3 -m pip install beautifulsoup4
sudo python3 -m pip install requests
sudo python3 -m pip install feedparser

rm -rf Homepage
git clone https://github.com/OlehKrupko/Homepage
python3 Homepage/manage.py runserver 192.168.1.201:8000