#!/usr/bin/env bash
set -xeE

sudo service gunicorn_every_election stop
sudo -u every_election /var/www/every_election/repo/serverscripts/rebuild_local_db.sh
sudo service gunicorn_every_election start
