#!/bin/bash
set -xeEo pipefail


# Optimise DB for replication
su -c "/var/www/polling_stations/postgres_writes_config.sh" - polling_stations
echo "fsync = off" | sudo tee -a /etc/postgresql/16/main/postgresql.conf
echo "wal_receiver_timeout = 12000" | sudo tee -a /etc/postgresql/16/main/postgresql.conf
echo "wal_receiver_create_temp_slot = 1" | sudo tee -a /etc/postgresql/16/main/postgresql.conf
INSTANCE_ID=$(curl http://instance-data/latest/meta-data/instance-id)
SUBSCRIPTION=polling_stations_${INSTANCE_ID:2}
echo "primary_slot_name = ${SUBSCRIPTION}" | sudo tee -a /etc/postgresql/16/main/postgresql.conf

sudo service postgresql restart

# Do the replication
su -c "/var/www/polling_stations/setup_db_replication.sh" - polling_stations

# Optimise DB for Reads
su -c "/var/www/polling_stations/postgres_reads_config.sh" - polling_stations
sudo service postgresql restart

sudo service polling_stations_gunicorn reload
