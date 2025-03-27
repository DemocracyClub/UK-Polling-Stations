#!/bin/bash

set -xeEo pipefail

mkdir -p /var/www/polling_stations/baked_elections/
# Always get the prod data, as we don't have stage or dev copies of this data yet.
aws s3 sync s3://pollingstations.private.data/addressbase/production/current_elections_parquet/ /var/www/polling_stations/baked_elections/
