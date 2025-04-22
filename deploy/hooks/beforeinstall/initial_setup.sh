#!/usr/bin/env bash
set -xeE

# These should match the values in deploy-env-vars.json
PROJECT_ROOT=/var/www/polling_stations
PROJECT_NAME=polling_stations

# --------
# apt bits
# --------

# Disable apt update timer
# Based on https://stackoverflow.com/questions/45269225/ansible-playbook-fails-to-lock-apt/51919678#51919678
# And https://unix.stackexchange.com/questions/463498/terminate-and-disable-remove-unattended-upgrade-before-command-returns
systemctl disable --now apt-daily.timer
systemctl disable --now apt-daily-upgrade.timer

rm -rf /var/lib/apt/lists/partial/*
mkdir -p /etc/systemd/system/apt-daily.timer.d
cat > /etc/systemd/system/apt-daily.timer.d/apt-daily.timer.conf <<- EOF
[Timer]
Persistent=false
EOF

# Wait for other upgrades to finish
systemd-run --property="After=apt-daily.service apt-daily-upgrade.service" --wait /bin/true

# Remove unattended upgrades
apt-get purge --yes unattended-upgrades

# Apt update
apt-get update --yes

# Let Apt do it's thing
while ps awx | grep --extended-regex 'apt[ -]' | grep -v grep
do
  echo "Waiting for existing apt process to finish"
  sleep 5
done
echo "Apt finished, continuing"


# Install apt packages
apt-get install --yes nginx nodejs npm gettext
npm install -g npm@9.9.4

# Reinstall unattended-upgrades
apt-get install --yes unattended-upgrades

# Restart apt update timer
systemctl start apt-daily.timer
systemctl daemon-reload


# -----------
# System User
# -----------

# Create User
id -u "$PROJECT_NAME" &>/dev/null || useradd --shell /bin/bash --create-home --home-dir "$PROJECT_ROOT"/home "$PROJECT_NAME"

# Permissions
mkdir -p $PROJECT_ROOT/code
chmod -R 755 "$PROJECT_ROOT"
chown -R "$PROJECT_NAME"  "$PROJECT_ROOT"


# -------------
# postgres bits
# -------------

# Make sure pg_hba.conf is permissive.
cat > /etc/postgresql/16/main/pg_hba.conf <<- EOF
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                trust
local   all             all                                     trust
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
EOF

# Create db user.
su postgres -c "createuser --superuser $PROJECT_NAME || true"
su postgres -c "createdb ${PROJECT_NAME} || true"
