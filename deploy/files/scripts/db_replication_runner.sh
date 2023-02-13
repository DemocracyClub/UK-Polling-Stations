#!/bin/bash
set -xeEo pipefail

su -c "/var/www/polling_stations/setup_db_replication.sh" - polling_stations
sudo service polling_stations_gunicorn reload
