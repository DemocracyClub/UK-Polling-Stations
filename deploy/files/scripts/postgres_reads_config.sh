#!/bin/bash
set -xeEo pipefail

DB_USER=${PROJECT_NAME}
DB=${PROJECT_NAME}

psql $DB -U $DB_USER -c "ALTER SYSTEM work_mem = '100MB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM shared_buffers = '512MB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM maintenance_work_mem = '1GB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM full_page_writes 'on'"
psql $DB -U $DB_USER -c "ALTER SYSTEM autovacuum 'on'"
psql $DB -U $DB_USER -c "ALTER SYSTEM wal_buffers '-1'"
psql $DB -U $DB_USER -c "ALTER SYSTEM effective_cache_size = '1024MB'"
psql $DB -U $DB_USER -c "ALTER SYSTEM checkpoint_completion_target = '0.9'"
psql $DB -U $DB_USER -c "ALTER SYSTEM default_statistics_target = '1000'"
