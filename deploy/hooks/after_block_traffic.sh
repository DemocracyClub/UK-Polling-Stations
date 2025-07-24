#!/usr/bin/env bash
set -xeuo pipefail

echo "Starting afterblocktraffic hook"

echo "Have a little sleep"
sleep 15
echo "wake up again and stop service"

systemctl stop polling_stations_db_replication.service

echo "Ending afterblocktraffic hook"
