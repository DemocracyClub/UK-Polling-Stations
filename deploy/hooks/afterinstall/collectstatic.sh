#!/usr/bin/env bash
set -xeE

cd /var/www/polling_stations/code/
uv run python manage.py collectstatic --noinput --clear
