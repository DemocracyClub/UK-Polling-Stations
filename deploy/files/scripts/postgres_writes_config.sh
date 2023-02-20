#!/bin/bash
set -xeEo pipefail

DB_USER=${PROJECT_NAME}
DB=${PROJECT_NAME}

psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM work_mem = '32MB'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM shared_buffers = '4GB'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM maintenance_work_mem = '2GB'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM full_page_writes = 'off'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM autovacuum = 'off'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM wal_buffers = '-1'"
