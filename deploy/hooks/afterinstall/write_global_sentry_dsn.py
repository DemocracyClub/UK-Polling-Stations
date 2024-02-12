#!/var/www/polling_stations/code/venv/bin/python

import sys

import boto3.exceptions
import botocore

client = boto3.client("ssm", region_name="eu-west-2")


try:
    sentry_dsn = client.get_parameter(Name="SENTRY_DSN")["Parameter"]["Value"]
except botocore.exceptions.ClientError:
    sys.exit("SENTRY_DSN not found")

with open("/etc/environment", "a") as env_file:
    env_file.write(f"""\nSENTRY_DSN="{sentry_dsn}"\n""")
