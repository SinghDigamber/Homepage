#!/bin/sh

### BEGIN INIT INFO
# Provides:          server-django-cacher.sh
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      1 0 6
# Short-Description: launches Django-cacher demon
### END INIT INFO

while sleep 10m; do curl "http://home.olehkrupko.com/bookUpdates/cache"; done