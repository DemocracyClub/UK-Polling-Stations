#!/bin/bash
set -xeEo pipefail

DB_USER=${PROJECT_NAME}
DB=${PROJECT_NAME}

psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM SET work_mem = '32MB'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM SET shared_buffers = '4GB'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM SET maintenance_work_mem = '2GB'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM SET full_page_writes = 'off'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM SET autovacuum = 'off'"
psql "$DB" -U "$DB_USER" -c "ALTER SYSTEM SET wal_buffers = '-1'"
