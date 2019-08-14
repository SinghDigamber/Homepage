#!/bin/sh

# setup Wi-Fi
touch "$path/wpa_supplicant.conf"
pathWiFi="$path/wpa_supplicant.conf"
read -r -p 'Wi-Fi network name (SSID): ' wifiName
read -r -p 'Wi-Fi password: ' wifiPassword
# write to file
echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" >> $pathWiFi
echo "update_config=1" >> $pathWiFi
echo "country=UA" >> $pathWiFi
echo "" >> $pathWiFi
echo "network={" >> $pathWiFi
echo "        ssid='$wifiName'" >> $pathWiFi
echo "        psk=\"$wifiPassword\"" >> $pathWiFi
echo "        key_mgmt=WPA-PSK" >> $pathWiFi
echo "}" >> $pathWiFi


sudo nano ~/.config/lxsession/LXDE-pi/autostart
# add:
@unclutter -idle 0.1
@chromium-browser --kiosk --noerrdialogs --profile=Default --app=https://youtube.com/tv

sudo apt update
sudo apt install postgresql

sudo systemctl status postgresql

sudo -i -u postgres
psql

