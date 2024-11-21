#!/bin/sh
set -e
set -x

if [ -z "$DC_ENVIRONMENT" ]; then
   echo "DC_ENVIRONMENT is not set"
   exit 1
fi

BUCKET_NAME="eoni-data.wheredoivote.co.uk.${DC_ENVIRONMENT}"
SRCDIR='/tmp/eoni_production_data'
PREM_4326_CSV=${SRCDIR}/PREM_4326.csv
PRO_4326_CSV=${SRCDIR}/PRO_4326.csv

LATEST_FILE=$(/usr/local/bin/aws s3 ls s3://"${BUCKET_NAME}/" | sort | tail -n1 | rev | cut -d' ' -f1 | rev)

if [ "$DC_ENVIRONMENT" = "production" ]; then
   SLACK_CHANNEL="bots"
else
   SLACK_CHANNEL="bot-testing"
fi

rm -rf $SRCDIR && mkdir -p $SRCDIR

/usr/local/bin/aws s3 cp s3://"${BUCKET_NAME}/${LATEST_FILE}" $SRCDIR

echo '"PREM_X_4326","PREM_Y_4326"' > ${PREM_4326_CSV}
mlr --icsv --otsv --headerless-csv-output cut -f PREM_X_COR,PREM_Y_COR $SRCDIR/"${LATEST_FILE}" |
	cs2cs -f "%.6f" +init=epsg:29902 +to +init=epsg:4326 |
	awk '{print "\""$1"\",\""$2"\""}' >> ${PREM_4326_CSV}

echo '"PRO_X_4326","PRO_Y_4326"' > ${PRO_4326_CSV}
mlr --icsv --otsv --headerless-csv-output cut -f PRO_X_COR,PRO_Y_COR $SRCDIR/"${LATEST_FILE}" |
	cs2cs -f "%.6f" +init=epsg:29902 +to +init=epsg:4326 |
	awk '{print "\""$1"\",\""$2"\""}'  >> ${PRO_4326_CSV}

paste -d ',' ${PRO_4326_CSV} ${PREM_4326_CSV} $SRCDIR/"${LATEST_FILE}" > eoni_reprojected.csv

/usr/bin/manage-py-command import_eoni --cleanup --reprojected --slack ${SLACK_CHANNEL} eoni_reprojected.csv

rm ${PREM_4326_CSV} ${PRO_4326_CSV} eoni_reprojected.csv
