#!/bin/bash

set -xeEo pipefail

set -a
source /var/www/polling_stations/code/.env
set +a

#### General Config #####
NAMESPACE="DemocracyClubCustomMetrics"
#### End General Config ####

#### DB_REPLICATION_SETUP_METRIC ####
RDS_CONNECTION_STRING="postgresql://postgres:${RDS_DB_PASSWORD}@${RDS_DB_HOST}/${RDS_DB_NAME}"
ACTIVE_REPLICATION_SLOTS=$(psql $RDS_CONNECTION_STRING -AXqtc "select count(*) from pg_replication_slots where active='t';")
INACTIVE_REPLICATION_SLOTS=$(psql $RDS_CONNECTION_STRING -AXqtc "select count(*) from pg_replication_slots where active='f';")
ACTIVE_JSON="{\"MetricName\":\"rds_active_replication_slot_count\",\"Value\":${ACTIVE_REPLICATION_SLOTS},\"Unit\":\"Count\"}"
INACTIVE_JSON="{\"MetricName\":\"rds_inactive_replication_slot_count\",\"Value\":${INACTIVE_REPLICATION_SLOTS},\"Unit\":\"Count\"}"

# Publish the metrics to CloudWatch
aws cloudwatch put-metric-data \
    --metric-data "[${ACTIVE_JSON},${INACTIVE_JSON}]" \
    --namespace "$NAMESPACE" \
