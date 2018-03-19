#!/bin/sh

# install Xcode with command line tools OR only tools with command:
xcode-select --install
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
### PyCharm install:
# Django
# beautifulsoup4
# collective.soupstrainer
# feedparser
# lxml
# requests

# not sure if works:
sudo python3 -m pip install django~=2.0.2 beautifulsoup4 collective.soupstrainer feedparser lxml requests

python3 ~/Homepage/manage.py migrate
python3 ~/Homepage/manage.py createsuperuser
