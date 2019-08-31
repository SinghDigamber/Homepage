#!/bin/sh

sudo apt-get install unclutter

pathAutostart='/etc/xdg/lxsession/LXDE-pi/autostart'
# add:
echo "@unclutter -idle 0.1" >> $pathAutostart
echo "@chromium-browser --kiosk --noerrdialogs --profile=Default --app=https://youtube.com/tv" >> $pathAutostart
