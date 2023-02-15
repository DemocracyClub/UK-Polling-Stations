#!/usr/bin/env bash
set -xeE

mv /var/www/polling_stations/code/deploy/files/conf/crontab /etc/cron.d/polling_stations_cron
chown root:root /etc/cron.d/polling_stations_cron
