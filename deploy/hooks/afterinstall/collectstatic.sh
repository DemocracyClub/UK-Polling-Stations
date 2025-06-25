#!/usr/bin/env bash
set -xeE

uv run python /var/www/polling_stations/code/manage.py collectstatic --noinput --clear
