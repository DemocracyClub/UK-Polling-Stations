#!/usr/bin/env bash
set -xeE

source /var/www/polling_stations/code/venv/bin/activate
cd /var/www/polling_stations/code/
python manage.py createcachetable
