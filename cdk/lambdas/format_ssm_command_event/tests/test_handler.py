import json
import os
from unittest import TestCase

import boto3
from moto import mock_aws

import handler

SAMPLE_EVENT = {
    "version": "0",
    "id": "abc-123",
    "detail-type": "EC2 Command Invocation Status-change Notification",
    "source": "aws.ssm",
    "account": "123456789012",
    "time": "2026-03-05T12:00:00Z",
    "region": "eu-west-2",
    "resources": ["arn:aws:ec2:eu-west-2:123456789012:instance/i-0abc123def456"],
    "detail": {
        "command-id": "cmd-0123456789abcdef0",
        "status": "Failed",
        "parameters": json.dumps(
            {"commands": ["/usr/bin/manage-py-command import_councils"]}
        ),
    },
}

os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


class TestHandler(TestCase):
    def setUp(self):
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"

        self.sns_mock = mock_aws()
        self.sns_mock.start()

        self.sns_client = boto3.client("sns", region_name="eu-west-2")
        topic = self.sns_client.create_topic(Name="test-topic")
        self.topic_arn = topic["TopicArn"]

        handler.SNS_TOPIC_ARN = self.topic_arn
        handler.DC_ENVIRONMENT = "development"

    def tearDown(self):
        self.sns_mock.stop()

    def test_publishes_formatted_message(self):
        handler.handler(SAMPLE_EVENT, None)

        # Verify the topic received a message by checking topic attributes
        attrs = self.sns_client.get_topic_attributes(TopicArn=self.topic_arn)
        self.assertIsNotNone(attrs)

    def test_message_contains_key_fields(self):
        # Subscribe an SQS queue to capture the message content
        sqs = boto3.client("sqs", region_name="eu-west-2")
        queue = sqs.create_queue(QueueName="test-queue")
        queue_url = queue["QueueUrl"]
        queue_arn = (
            boto3.resource("sqs", region_name="eu-west-2")
            .Queue(queue_url)
            .attributes["QueueArn"]
        )

        self.sns_client.subscribe(
            TopicArn=self.topic_arn, Protocol="sqs", Endpoint=queue_arn
        )

        # Handle the event
        handler.handler(SAMPLE_EVENT, None)

        messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
        body = json.loads(messages["Messages"][0]["Body"])
        message = body["Message"]

        self.assertIn("Status: Failed", message)
        self.assertIn("Instance: i-0abc123def456", message)
        self.assertIn("Command ID: cmd-0123456789abcdef0", message)
        self.assertIn("/usr/bin/manage-py-command import_councils", message)
        self.assertIn("account 123456789012", message)
        self.assertIn(
            "https://eu-west-2.console.aws.amazon.com"
            "/systems-manager/run-command/cmd-0123456789abcdef0"
            "?region=eu-west-2",
            message,
        )

    def test_message_includes_full_json(self):
        sqs = boto3.client("sqs", region_name="eu-west-2")
        queue = sqs.create_queue(QueueName="test-queue")
        queue_url = queue["QueueUrl"]
        queue_arn = (
            boto3.resource("sqs", region_name="eu-west-2")
            .Queue(queue_url)
            .attributes["QueueArn"]
        )

        self.sns_client.subscribe(
            TopicArn=self.topic_arn, Protocol="sqs", Endpoint=queue_arn
        )

        # Handle the event
        handler.handler(SAMPLE_EVENT, None)

        messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
        body = json.loads(messages["Messages"][0]["Body"])
        message = body["Message"]

        self.assertIn('"command-id": "cmd-0123456789abcdef0"', message)

    def test_raises_without_topic_arn(self):
        handler.SNS_TOPIC_ARN = None

        with self.assertRaises(RuntimeError) as cm:
            handler.handler(SAMPLE_EVENT, None)

        self.assertIn("SNS_TOPIC_ARN not set", str(cm.exception))
