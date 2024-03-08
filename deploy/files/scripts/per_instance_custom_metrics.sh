#!/bin/bash

set -xeEo pipefail

set -a
source /var/www/polling_stations/code/.env
set +a

#### General Config #####
NAMESPACE="DemocracyClubCustomMetrics"
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
#### End General Config ####


#### DB_REPLICATION_SETUP_METRIC ####
SERVICE_NAME=${PROJECT_NAME}_db_replication.service
# Check if the service is active
systemctl is-active --quiet $SERVICE_NAME
SERVICE_STATUS=$?
# Convert the status to a metric, e.g., 1 for active, 0 for inactive
DB_REPLICATION_SETUP_METRIC=$([[ $SERVICE_STATUS -eq 0 ]] && echo 1 || echo 0)

# Publish the metric to CloudWatch
aws cloudwatch put-metric-data \
    --metric-name "${SERVICE_NAME}.status" \
    --namespace "$NAMESPACE" \
    --value "$DB_REPLICATION_SETUP_METRIC" \
    --unit "None" \
    --dimensions "InstanceId=${INSTANCE_ID}" \
#### END DB_REPLICATION_SETUP_METRIC ####
