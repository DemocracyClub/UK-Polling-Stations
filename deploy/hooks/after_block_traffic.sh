#!/usr/bin/env bash
set -xeuo pipefail

systemctl stop polling_stations_db_replication.service
