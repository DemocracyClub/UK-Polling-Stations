#!/usr/bin/env bash
set -xeE

# These should match the values in deploy-env-vars.json
PROJECT_ROOT=/var/www/polling_stations
PROJECT_NAME=polling_stations

# --------
# apt bits
# --------

# Disable apt update timer
systemctl disable apt-daily.timer
rm -rf /var/lib/apt/lists/partial/*
mkdir -p /etc/systemd/system/apt-daily.timer.d
cat > /etc/systemd/system/apt-daily.timer.d/apt-daily.timer.conf <<- EOF
[Timer]
Persistent=false
EOF

# Let Apt do it's thing
while ps awx | grep "apt[ -]" | grep -v grep
do
  echo "Waiting for existing apt process to finish"
  sleep 5
done
echo "Apt finished, continuing"

# Install apt packages
apt-get update
apt-get install --yes nginx nodejs npm gettext

# Install cloudwatch
mkdir -p /tmp/cloudwatch-logs
cd /tmp/cloudwatch-logs
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb

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
cat > /etc/postgresql/14/main/pg_hba.conf <<- EOF
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
