#!/bin/bash
set -xeEo pipefail

set -a
source /var/www/polling_stations/code/.env
set +a

# rotate the log file otherwise output is lost in cloudwatch
echo "" > /var/log/db_replication/logs.log

DB_USER=${PROJECT_NAME}
DB=${PROJECT_NAME}
METADATA_TOKEN=$(curl -X PUT "http://instance-data/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" --fail --silent)
INSTANCE_ID=$(curl "http://instance-data/latest/meta-data/instance-id" -H "X-aws-ec2-metadata-token: $METADATA_TOKEN" --fail --silent)
SUBSCRIPTION=${USER}_${INSTANCE_ID:2}

# Set up DB and enable PostGIS
dropdb --if-exists "$DB" -U "$DB_USER"
createdb "$DB" -U "$DB_USER"
psql "$DB" -U "$DB_USER" -c 'create extension postgis;'


# Activate Virtual env
source /var/www/polling_stations/code/venv/bin/activate

# Migrate db - this builds the schema before syncing
/var/www/polling_stations/code/manage.py migrate --database=local

# Truncate some tables that are populated by the above steps
psql "$DB" -U "$DB_USER" -c 'TRUNCATE "spatial_ref_sys", "auth_permission", "django_migrations", "django_content_type", "django_site" RESTART IDENTITY CASCADE;'

# Drop constraints to improve sync time
psql "$DB" -U "$DB_USER" -c 'alter table addressbase_address drop constraint addressbase_address_pkey cascade;'
psql "$DB" -U "$DB_USER" -c 'alter table addressbase_uprntocouncil drop constraint addressbase_uprntocouncil_pkey cascade;'
psql "$DB" -U "$DB_USER" -c 'DROP INDEX address_location_gist, address_postcode_idx, address_postcode_like_idx, address_uprn_like_idx, uprntocouncil_adv_v_station_idx, uprntocouncil_uprn_like_idx, uprntocouncil_lad_idx;'

# Set up subscription
psql "$DB" -U "$DB_USER" -c "CREATE SUBSCRIPTION $SUBSCRIPTION CONNECTION 'dbname=$RDS_DB_NAME host=$RDS_DB_HOST user=postgres password=$RDS_DB_PASSWORD' PUBLICATION alltables with (streaming=true, binary=true);"

# Wait for all tables to finish initial sync
echo "starting initial db sync"
WORKER_STATS=""
while [ "$WORKER_STATS" != "r" ]
do
    WORKER_STATS=$(psql polling_stations -U polling_stations -AXqtc "select string_agg(distinct srsubstate, '' order by srsubstate) from pg_subscription_rel;")
    sleep 15
    if [ "$WORKER_STATS" = "fr" ]; then
      psql "$DB" -U "$DB_USER" -c "DROP SUBSCRIPTION $SUBSCRIPTION;"
      psql "$DB" -U "$DB_USER" -c "CREATE SUBSCRIPTION $SUBSCRIPTION CONNECTION 'dbname=$RDS_DB_NAME host=$RDS_DB_HOST user=postgres password=$RDS_DB_PASSWORD' PUBLICATION alltables with (streaming=true, binary=true, copy_data=false);"
    fi
done
echo "initial db sync complete"

echo "Rebuilding indexes..."
# Rebuild constraints
psql "$DB" -U "$DB_USER" -c 'ALTER TABLE addressbase_address ADD PRIMARY KEY (uprn);'
psql "$DB" -U "$DB_USER" -c 'ALTER TABLE addressbase_uprntocouncil ADD PRIMARY KEY (uprn);'
psql "$DB" -U "$DB_USER" -c 'ALTER TABLE addressbase_uprntocouncil ADD CONSTRAINT uprntocouncil_uprn_fk_address_uprn FOREIGN KEY (uprn) REFERENCES addressbase_address (uprn) MATCH FULL;'

# Rebuild Indexes
psql "$DB" -U "$DB_USER" -c 'CREATE INDEX address_location_gist ON public.addressbase_address USING gist (location);'
psql "$DB" -U "$DB_USER" -c 'CREATE INDEX address_postcode_idx ON public.addressbase_address USING btree (postcode);'
psql "$DB" -U "$DB_USER" -c 'CREATE INDEX address_postcode_like_idx ON public.addressbase_address USING btree (postcode varchar_pattern_ops);'
psql "$DB" -U "$DB_USER" -c 'CREATE INDEX address_uprn_like_idx ON public.addressbase_address USING btree (uprn varchar_pattern_ops);'
psql "$DB" -U "$DB_USER" -c 'CREATE INDEX uprntocouncil_adv_v_station_idx ON public.addressbase_uprntocouncil USING btree (advance_voting_station_id);'
psql "$DB" -U "$DB_USER" -c 'CREATE INDEX uprntocouncil_uprn_like_idx ON public.addressbase_uprntocouncil USING btree (uprn varchar_pattern_ops);'
psql "$DB" -U "$DB_USER" -c 'CREATE INDEX uprntocouncil_lad_idx ON public.addressbase_uprntocouncil USING btree (lad);'

echo "...indexes rebuilt. Analyzing..."

psql "$DB" -U "$DB_USER" -c 'ANALYZE;'

echo "...ANALYZE complete, DB ready for reads."

touch ~/db_replication_complete
