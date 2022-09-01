#!/usr/bin/env bash
set -xeE

# enabling will allow the services to start if the instance reboots
systemctl enable polling_stations_db_replication.service
systemctl enable polling_stations_gunicorn.socket

systemctl start polling_stations_db_replication.service
systemctl start polling_stations_gunicorn.socket
