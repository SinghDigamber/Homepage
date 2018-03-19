#!/bin/sh

### BEGIN INIT INFO
# Provides:          server-django.sh
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      1 0 6
# Short-Description: launches Django demon
### END INIT INFO

rm -rf /home/pi/Projects/Homepage
git clone https://github.com/OlehKrupko/Homepage /home/pi/Projects/Homepage
python3 /home/pi/Projects/Homepage/manage.py runserver 192.168.1.201:8000