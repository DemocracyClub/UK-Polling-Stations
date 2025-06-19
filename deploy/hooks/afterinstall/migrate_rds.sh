#!/usr/bin/env bash
set -xeE

cd /var/www/polling_stations/code/
uv run manage.py migrate --database=principal --noinput
