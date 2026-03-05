import json
import logging
import os
import textwrap

import boto3
import sentry_sdk

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
DC_ENVIRONMENT = os.environ.get("DC_ENVIRONMENT")
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

if SENTRY_DSN:
    sentry_sdk.init(SENTRY_DSN)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("Received EventBridge event: %s", json.dumps(event))

    detail = event.get("detail", {})
    status = detail.get("status", "UNKNOWN")
    event_time = event.get("time", "UNKNOWN")
    detail_type = event.get("detail-type", "UNKNOWN")
    region = event.get("region", "UNKNOWN")
    account = event.get("account", "UNKNOWN")
    command_id = detail.get("command-id", "UNKNOWN")

    # Extract instance ID from the resource ARN if present
    # ARN format: arn:aws:ec2:region:account:instance/i-xxx
    resources = event.get("resources", [])
    instance_id = "UNKNOWN"
    for resource in resources:
        if ":instance/" in resource:
            instance_id = resource.split("/")[-1]
            break

    # Extract the shell command from the parameters field
    # parameters is a JSON-encoded string like '{"commands":["some-command"]}'
    command_text = "UNKNOWN"
    try:
        parameters = json.loads(detail.get("parameters", "{}"))
        commands = parameters.get("commands", [])
        if commands:
            command_text = "\n".join(commands)
    except (json.JSONDecodeError, TypeError):
        pass

    console_url = (
        f"https://{region}.console.aws.amazon.com"
        f"/systems-manager/run-command/{command_id}?region={region}"
    )

    event_json = json.dumps(event, indent=2)

    message = textwrap.dedent(f"""\
        SSM Command {status} on {DC_ENVIRONMENT}

        Status: {status}
        Time: {event_time}
        Event type: {detail_type}
        Instance: {instance_id}
        Command ID: {command_id}

        Command:
            {command_text}
        AWS Console (account {account}):
          {console_url}


        Full event JSON:
            {event_json}
    """)

    if SNS_TOPIC_ARN is None:
        raise RuntimeError("SNS_TOPIC_ARN not set; cannot publish")

    sns = boto3.client("sns")
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject=f"({DC_ENVIRONMENT}) SSM Command {status}",
    )
    logger.info("Published formatted message to SNS")
