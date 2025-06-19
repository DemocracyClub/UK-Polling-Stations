#!/usr/bin/env bash
set -xeE


# Create a virtualenv
cd /var/www/polling_stations/code/

uv sync --group production --no-group dev --no-group cdk
