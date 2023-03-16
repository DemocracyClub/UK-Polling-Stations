#!/bin/bash
set -xeEo pipefail

DB_USER=${PROJECT_NAME}
DB=${PROJECT_NAME}

psql $DB -U $DB_USER -c "ALTER SYSTEM SET work_mem = '100MB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET shared_buffers = '512MB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET maintenance_work_mem = '1GB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET full_page_writes = on"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET autovacuum = on"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET wal_buffers = '-1'"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET effective_cache_size = '1024MB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET checkpoint_completion_target = '0.9'"
psql $DB -U $DB_USER -c "ALTER SYSTEM SET default_statistics_target = '1000'"
