#!/var/www/polling_stations/code/.venv/bin/python

import sys

import boto3.exceptions
import botocore

client = boto3.client("ssm", region_name="eu-west-2")

vars = {"SENTRY_DSN": "", "DC_ENVIRONMENT": ""}


for var in vars:
    try:
        value = client.get_parameter(Name=var)["Parameter"]["Value"]
    except botocore.exceptions.ClientError:
        sys.exit(f"{var} not found")
    vars[var] = value


with open("/etc/environment", "a") as env_file:
    for key, value in vars.items():
        env_file.write(f"""\n{key}="{value}"\n""")
