#!/usr/bin/env bash
set -xeE

cd /var/www/polling_stations/code/
sudo npm install -g npm@9.9.4
npm ci
