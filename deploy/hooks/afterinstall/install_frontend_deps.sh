#!/usr/bin/env bash
set -xeE

cd /var/www/polling_stations/code/
UV_USE_IO_URING=0 npm ci
