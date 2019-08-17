cat ~/Projects/Homepage/scripts/homepage.prepeDjango.sh | ssh -p 8022 pi@krupko.space

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
