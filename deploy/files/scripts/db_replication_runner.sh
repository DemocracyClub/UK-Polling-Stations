#!/bin/bash
set -xeEo pipefail


# Optimise DB for replication
su -c "/var/www/polling_stations/postgres_writes_config.sh" - polling_stations
echo "fsync = off" | sudo tee -a /etc/postgresql/14/main/postgresql.conf
sudo service postgresql restart

# Do the replication
su -c "/var/www/polling_stations/setup_db_replication.sh" - polling_stations

# Optimise DB for Reads
su -c "/var/www/polling_stations/postgres_reads_config.sh" - polling_stations
sudo service postgresql restart

sudo service polling_stations_gunicorn reload
