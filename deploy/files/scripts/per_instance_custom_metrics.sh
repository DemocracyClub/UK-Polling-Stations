#!/bin/bash

set -xeEo pipefail

set -a
source /var/www/polling_stations/code/.env
set +a

#### General Config #####
NAMESPACE="DemocracyClubCustomMetrics"
METADATA_TOKEN=$(curl -X PUT "http://instance-data/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" --fail --silent)
INSTANCE_ID=$(curl "http://instance-data/latest/meta-data/instance-id" -H "X-aws-ec2-metadata-token: $METADATA_TOKEN" --fail --silent)
INSTANCE_DIMENSION="[{\"Name\":\"InstanceId\",\"Value\":\"${INSTANCE_ID}\"}]"
#### End General Config ####

#### DB REPLICATION SETUP METRIC ####
SERVICE_NAME=${PROJECT_NAME}_db_replication.service
# Check if the service is active
systemctl is-active --quiet $SERVICE_NAME
SERVICE_STATUS=$?
# Convert the status to a metric, e.g., 1 for active, 0 for inactive
DB_REPLICATION_SETUP_METRIC=$([[ $SERVICE_STATUS -eq 0 ]] && echo 1 || echo 0)
DRSM_JSON="{\"MetricName\":\"${SERVICE_NAME}.status\",\"Value\":${DB_REPLICATION_SETUP_METRIC},\"Dimensions\":${INSTANCE_DIMENSION}}"
#### END DB REPLICATION SETUP METRIC ####

#### DB REPLICATION COMPLETE METRIC ####
INITIAL_REPLICATION_COMPLETE_PATH="/var/www/polling_stations/home/db_replication_complete"

if [ -f "$INITIAL_REPLICATION_COMPLETE_PATH" ]; then
    INITIAL_DB_REPLICATION_COMPLETE_METRIC=1
else
    INITIAL_DB_REPLICATION_COMPLETE_METRIC=0
fi
IDRC_JSON_1="{\"MetricName\":\"replication-complete-file-exists\",\"Value\":${INITIAL_DB_REPLICATION_COMPLETE_METRIC},\"Dimensions\":${INSTANCE_DIMENSION}}"
IDRC_JSON_2="{\"MetricName\":\"replication-complete-file-exists\",\"Value\":${INITIAL_DB_REPLICATION_COMPLETE_METRIC}}"

#### DB REPLICATION COMPLETE METRIC ####


# Publish the metric to CloudWatch
aws cloudwatch put-metric-data \
    --metric-data "[${DRSM_JSON},${IDRC_JSON_1},${IDRC_JSON_2}]" \
    --namespace "$NAMESPACE"
