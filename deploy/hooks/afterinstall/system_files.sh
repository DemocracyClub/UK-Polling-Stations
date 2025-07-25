#!/usr/bin/env bash
set -xeE

set -a
source /var/www/polling_stations/code/.env
METADATA_TOKEN=$(curl -X PUT "http://instance-data/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" --fail --silent)
INSTANCE_ID=$(curl "http://instance-data/latest/meta-data/instance-id" -H "X-aws-ec2-metadata-token: $METADATA_TOKEN" --fail --silent)
set +a

SYSTEMD_SRC="${PROJECT_ROOT}/code/deploy/files/systemd"
SYSTEMD_DST="/etc/systemd/system"
CONF_SRC="${PROJECT_ROOT}/code/deploy/files/conf"

# ----------
# cloudwatch
# ----------
envsubst '$INSTANCE_ID=$(curl "http://instance-data/latest/meta-data/instance-id" -H "X-aws-ec2-metadata-token: $METADATA_TOKEN" --fail --silent)' < "$CONF_SRC"/cloudwatch.json > /root/.cloudwatch.json
envsubst  '$PROJECT_NAME $PROJECT_ROOT $APP_NAME' < "$SYSTEMD_SRC"/cloudwatch.service > ${SYSTEMD_DST}/"$PROJECT_NAME"_cloudwatch.service
chmod 0644 /root/.cloudwatch.json
systemctl enable "$PROJECT_NAME"_cloudwatch.service
systemctl start "$PROJECT_NAME"_cloudwatch.service


# -------
# Scripts
# -------
for script in "$PROJECT_ROOT"/code/deploy/files/scripts/*.sh; do
  script_name=$(basename "$script")
  # shellcheck disable=SC2016
  envsubst '$PROJECT_NAME $PROJECT_ROOT $DC_ENVIRONMENT' < "$script" > "$PROJECT_ROOT"/"$script_name"
  chmod 755 "$PROJECT_ROOT"/"$script_name"
done

for script in "$PROJECT_ROOT"/code/deploy/files/scripts/user_scripts/*; do
  script_name=$(basename "$script")
  # shellcheck disable=SC2016
  envsubst '$PROJECT_NAME' < "$script" > /usr/bin/"$script_name"
  chmod 755 /usr/bin/"$script_name"
done

# -------------
# Service files
# -------------
for service in "$SYSTEMD_SRC"/*.service; do
  service_name="$PROJECT_NAME"_$(basename "$service")
  # shellcheck disable=SC2016
  envsubst '$PROJECT_NAME $PROJECT_ROOT $APP_NAME' < "$service" > ${SYSTEMD_DST}/"$service_name"
done

# ------
# Socket
# ------
# shellcheck disable=SC2016
envsubst '$PROJECT_NAME' < "$SYSTEMD_SRC"/gunicorn.socket > "$SYSTEMD_DST"/"$PROJECT_NAME"_gunicorn.socket

# -----------------
# Gunicorn tmpfiles
# -----------------
# shellcheck disable=SC2016
envsubst '$PROJECT_NAME' < "$SYSTEMD_SRC"/gunicorn.tmpfiles > /etc/tmpfiles.d/"$PROJECT_NAME"_gunicorn.conf
systemd-tmpfiles --create

# ------
# bashrc
# ------
echo 'cd && cd ../code && source .venv/bin/activate' > "$PROJECT_ROOT"/home/.bashrc

# --------------------
# replication log file
# --------------------
mkdir -p /var/log/db_replication && chmod 0777 /var/log/db_replication
touch /var/log/db_replication/logs.log && chmod 0777 /var/log/db_replication/logs.log

# -----
# nginx
# -----
rm -f /etc/nginx/sites-enabled/default
# shellcheck disable=SC2016
envsubst '$PROJECT_NAME $PROJECT_ROOT $APP_NAME' < "$CONF_SRC"/nginx.conf > /etc/nginx/sites-enabled/"$PROJECT_NAME"
systemctl restart nginx
