#!/bin/sh

# static
imagePath='/Users/olehkrupko/Projects/Homepage-files/prepareSD/2019-07-10-raspbian-buster.img'

# burn image
# https://www.raspberrypi.org/documentation/installation/installing-images/mac.md
printf 'Here are the disks mounted:\n'
diskutil list
read -r -p 'Type in disk# that has to be used (e.g. disk4, not disk4s1): ' diskN
diskutil unmountDisk "/dev/disk$diskN"
printf 'Starting to burn image...\n'
sudo dd bs=1m if=$imagePath of="/dev/rdisk$diskN" conv=sync
printf 'Image burnt.\n'
diskutil mountDisk "/dev/disk$diskN"

# enable SSH
printf 'Here are the Volumes mounted:\n'
ls /Volumes  # check for sd card name
read -r -p 'Type in Volume name that has to be used: ' path
path="/Volumes/$path"
touch "$path/ssh"  # sd card name is 'boot' in this case

# setup Wi-Fi
touch "$path/wpa_supplicant.conf"
pathWiFi="$path/wpa_supplicant.conf"
touch pathWiFi
read -r -p 'Wi-Fi network name (SSID): ' wifiName
read -r -p 'Wi-Fi password: ' wifiPassword
# write to file
echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" >> $pathWiFi
echo "update_config=1" >> $pathWiFi
echo "country=UA" >> $pathWiFi
echo "" >> $pathWiFi
echo "network={" >> $pathWiFi
echo "        ssid=\"$wifiName\"" >> $pathWiFi
echo "        psk=\"$wifiPassword\"" >> $pathWiFi
echo "}" >> $pathWiFi

diskutil unmount /Volumes/boot  # unmount sd card