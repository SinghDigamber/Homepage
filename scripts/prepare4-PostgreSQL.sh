#!/bin/sh
# Postgre logs are at tail /var/log/postgresql/postgresql-x.x-main.log

sudo apt-get update
sudo apt install postgresql

ls /etc/postgresql/
sudo nano /etc/postgresql/11/main/pg_hba.conf
# Add the following line to the configuration file:
host    all             all             192.168.1.200/24        trust
host    all             all             192.168.1.201/24        trust

sudo nano /etc/postgresql/11/main/postgresql.conf
# Find the following line
listen_addresses='localhost'
#Change it to
listen_addresses='*'

sudo systemctl restart postgresql

sudo su - postgres
psql

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
