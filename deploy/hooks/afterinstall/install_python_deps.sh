#!/usr/bin/env bash
set -xeE


# Create a virtualenv
cd /var/www/polling_stations/code/
python3 -m venv venv

# Activate the virtualenv
source /var/www/polling_stations/code/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install --requirement /var/www/polling_stations/code/requirements/production.txt
