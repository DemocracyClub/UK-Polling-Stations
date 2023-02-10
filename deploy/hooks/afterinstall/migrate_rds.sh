#!/usr/bin/env bash
set -xeE

source /var/www/polling_stations/code/venv/bin/activate
python /var/www/polling_stations/code/manage.py migrate --database=principal --noinput
