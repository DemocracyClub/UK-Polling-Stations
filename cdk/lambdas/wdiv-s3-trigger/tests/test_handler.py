import io
import json
import os
import sys
from pathlib import Path
from unittest import TestCase

import boto3
import moto
import pytest
import responses
from botocore.exceptions import ClientError
from councils.tests.factories import CouncilFactory
from file_uploads.api import UploadSerializer
from moto import mock_aws
from moto.s3 import responses as moto_s3_responses
from moto.ses import ses_backends
from trigger.handler import main

trigger_payload_str = """{
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "eu-west-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "fake-upload-bucket",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::fake-upload-bucket"
        },
        "object": {
          "key": "X01000000/2019-12-12/2019-09-30T17%3A00%3A02.396833/data.csv",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}"""
trigger_payload = json.loads(trigger_payload_str)

ios_payload = json.loads(trigger_payload_str.replace("X01000000", "IOS"))

os.environ["AWS_DEFAULT_REGION"] = moto_s3_responses.DEFAULT_REGION_NAME = "eu-west-1"


@pytest.mark.django_db
class HandlerTests(TestCase):
    """
    This is a very high-level integration test touching most of the codebase.
    In general, this codebase reaches out to a lot of external services,
    so there is a lot of mocking to be done.

    As we add additional interactions and associated credentials,
    its important to remember to remember to add mocks for them.
    Responses should help with this by throwing
    `Connection refused by Responses: POST https://thing.i/didnt/mock/yet doesn't match Responses Mock`
    """

    def setUp(self):
        # ensure we definitely don't have any real credentials set for AWS
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"

        # don't send errors to senty under test
        os.environ["SENTRY_DSN"] = ""

        # set fake credentials for services
        # we're going to have mocked interactions with
        self.repo = "chris48s/does-not-exist"
        self.upload_bucket = "fake-upload-bucket"
        self.final_bucket = "fake-final-bucket"
        region = "eu-west-1"
        os.environ["GITHUB_REPO"] = self.repo
        os.environ["GITHUB_API_KEY"] = "testing"
        os.environ["WDIV_API_KEY"] = "testing"
        os.environ["FINAL_BUCKET_NAME"] = self.final_bucket
        os.environ["AWS_REGION"] = region
        os.environ["ERROR_REPORT_EMAIL"] = "fred@example.com"
        os.environ["WDIV_WEBHOOK_URL"] = "https://wheredoivote.co.uk/api/beta/uploads/"

        # set up pretend s3 bucket
        self.s3mock = mock_aws()
        self.s3mock.start()
        self.conn = boto3.client("s3")
        self.conn.create_bucket(Bucket=self.upload_bucket)
        self.conn.create_bucket(Bucket=self.final_bucket)

        # mock SES
        self.sesmock = mock_aws()
        self.sesmock.start()
        conn = boto3.client("ses", region)
        conn.verify_email_identity(EmailAddress="pollingstations@democracyclub.org.uk")

        # mock all the HTTP responses we're going to make
        responses.start()
        responses.add(
            responses.GET,
            "https://wheredoivote.co.uk/api/beta/councils/X01000000.json/?auth_token=testing",
            status=200,
            body=json.dumps({"name": "Piddleton Parish Council"}),
        )
        responses.add(
            responses.GET,
            "https://wheredoivote.co.uk/api/beta/councils/IOS.json/?auth_token=testing",
            status=200,
            body=json.dumps({"name": "Isle of Wight Council"}),
        )
        responses.add(
            responses.GET,
            f"https://api.github.com/repos/{self.repo}/issues?state=open&labels=Data%20Import",
            json=[],
            status=200,
        )
        responses.add(
            responses.POST,
            f"https://api.github.com/repos/{self.repo}/issues",
            json={"html_url": f"https://github.com/{self.repo}/issues/1"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://wheredoivote.co.uk/api/beta/uploads/",
            json={},
            status=200,
        )
        CouncilFactory(
            **{
                "council_id": "X01000000",
            }
        )
        CouncilFactory(
            **{
                "council_id": "IOS",
            }
        )

        sys.stdout = io.StringIO()

    def tearDown(self):
        responses.stop()
        responses.reset()
        self.s3mock.stop()
        self.sesmock.stop()
        sys.stdout = sys.__stdout__

    def load_fixture(
        self, filename, key="data.csv", mimetype=None, council_id="X01000000"
    ):
        # load a fixture into our pretend S3 bucket
        def guess_content_type(filename):
            return (
                "text/tab-separated-values"
                if filename.lower().endswith(".tsv")
                else "text/csv"
            )

        if not mimetype:
            mimetype = guess_content_type(filename)
        fixture_path = Path(__file__).parent / "fixtures" / filename
        fixture = fixture_path.open().read()
        self.conn.put_object(
            Bucket=self.upload_bucket,
            Key=f"{council_id}/2019-12-12/2019-09-30T17:00:02.396833/{key}",
            Body=fixture,
            ContentType=mimetype,
        )

    def test_valid_one_file(self):
        self.load_fixture("ems-idox-eros.csv")

        main(trigger_payload, None)

        self.assertEqual(4, len(responses.calls))
        self.assertEqual(
            f"https://api.github.com/repos/{self.repo}/issues",
            responses.calls[2].request.url,
        )
        self.assertEqual(
            "https://wheredoivote.co.uk/api/beta/uploads/",
            responses.calls[3].request.url,
        )
        expected_dict = {
            "github_issue": f"https://github.com/{self.repo}/issues/1",
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "timestamp": "2019-09-30T17:00:02.396833",
            "election_date": "2019-12-12",
            "file_set": [
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/data.csv",
                    "csv_valid": True,
                    "csv_rows": 10,
                    "csv_encoding": "utf-8",
                    "ems": "Idox Eros (Halarose)",
                    "errors": "",
                }
            ],
        }

        upload_serializer = UploadSerializer(data=expected_dict)
        self.assertTrue(upload_serializer.is_valid(raise_exception=True))

        self.assertDictEqual(expected_dict, json.loads(responses.calls[3].request.body))
        resp = self.conn.get_object(
            Bucket=self.final_bucket,
            Key="X01000000/2019-12-12/2019-09-30T17:00:02.396833/report.json",
        )
        self.assertEqual(expected_dict, json.loads(resp["Body"].read()))
        ses_backend = ses_backends[moto.core.DEFAULT_ACCOUNT_ID][
            os.environ.get("AWS_DEFAULT_REGION")
        ]
        self.assertEqual(0, len(ses_backend.sent_messages))

    def test_valid_democracy_counts(self):
        self.load_fixture("ems-dcounts-stations.csv", "ems-dcounts-stations.csv")
        self.load_fixture("ems-dcounts-districts.csv", "ems-dcounts-districts.csv")

        main(trigger_payload, None)

        self.assertEqual(4, len(responses.calls))
        self.assertEqual(
            f"https://api.github.com/repos/{self.repo}/issues",
            responses.calls[2].request.url,
        )
        self.assertEqual(
            "https://wheredoivote.co.uk/api/beta/uploads/",
            responses.calls[3].request.url,
        )
        expected_dict = {
            "github_issue": f"https://github.com/{self.repo}/issues/1",
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "timestamp": "2019-09-30T17:00:02.396833",
            "election_date": "2019-12-12",
            "file_set": [
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/ems-dcounts-districts.csv",
                    "csv_valid": True,
                    "csv_rows": 20,
                    "csv_encoding": "utf-8",
                    "ems": "Democracy Counts",
                    "errors": "",
                },
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/ems-dcounts-stations.csv",
                    "csv_valid": True,
                    "csv_rows": 20,
                    "csv_encoding": "utf-8",
                    "ems": "Democracy Counts",
                    "errors": "",
                },
            ],
        }

        upload_serializer = UploadSerializer(data=expected_dict)
        self.assertTrue(upload_serializer.is_valid(raise_exception=True))

        self.assertDictEqual(expected_dict, json.loads(responses.calls[3].request.body))
        resp = self.conn.get_object(
            Bucket=self.final_bucket,
            Key="X01000000/2019-12-12/2019-09-30T17:00:02.396833/report.json",
        )
        self.assertEqual(expected_dict, json.loads(resp["Body"].read()))
        ses_backend = ses_backends[moto.core.DEFAULT_ACCOUNT_ID][
            os.environ.get("AWS_DEFAULT_REGION")
        ]
        self.assertEqual(0, len(ses_backend.sent_messages))

    def test_democracy_counts_small(self):
        self.load_fixture(
            "ems-dcounts-stations-small.csv", "ems-dcounts-stations-small.csv"
        )
        self.load_fixture("ems-dcounts-districts.csv", "ems-dcounts-districts.csv")

        main(trigger_payload, None)

        self.assertEqual(2, len(responses.calls))

        expected_dict = {
            "github_issue": "",
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "timestamp": "2019-09-30T17:00:02.396833",
            "election_date": "2019-12-12",
            "file_set": [
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/ems-dcounts-districts.csv",
                    "csv_valid": True,
                    "csv_rows": 20,
                    "csv_encoding": "utf-8",
                    "ems": "Democracy Counts",
                    "errors": "",
                },
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/ems-dcounts-stations-small.csv",
                    "csv_valid": False,
                    "csv_rows": 0,
                    "csv_encoding": "",
                    "ems": "unknown",
                    "errors": "Expected file to be at least 1KB",
                },
            ],
        }

        upload_serializer = UploadSerializer(data=expected_dict)
        self.assertTrue(upload_serializer.is_valid(raise_exception=True))

        self.assertDictEqual(expected_dict, json.loads(responses.calls[1].request.body))
        with self.assertRaises(ClientError):
            self.conn.get_object(
                Bucket=self.final_bucket,
                Key="X01000000/2019-09-30T17:00:02.396833/report.json",
            )
        ses_backend = ses_backends[moto.core.DEFAULT_ACCOUNT_ID][
            os.environ.get("AWS_DEFAULT_REGION")
        ]
        self.assertEqual(1, len(ses_backend.sent_messages))

    def test_valid_democracy_counts_small(self):
        self.load_fixture(
            "ems-dcounts-stations.csv",
            "ems-dcounts-stations-small.csv",
            council_id="IOS",
        )
        self.load_fixture(
            "ems-dcounts-districts.csv", "ems-dcounts-districts.csv", council_id="IOS"
        )
        main(ios_payload, None)

        self.assertEqual(4, len(responses.calls))
        self.assertEqual(
            f"https://api.github.com/repos/{self.repo}/issues",
            responses.calls[2].request.url,
        )
        self.assertEqual(
            "https://wheredoivote.co.uk/api/beta/uploads/",
            responses.calls[3].request.url,
        )
        expected_dict = {
            "github_issue": f"https://github.com/{self.repo}/issues/1",
            "gss": "IOS",
            "council_name": "Isle of Wight Council",
            "timestamp": "2019-09-30T17:00:02.396833",
            "election_date": "2019-12-12",
            "file_set": [
                {
                    "key": "IOS/2019-12-12/2019-09-30T17:00:02.396833/ems-dcounts-districts.csv",
                    "csv_valid": True,
                    "csv_rows": 20,
                    "csv_encoding": "utf-8",
                    "ems": "Democracy Counts",
                    "errors": "",
                },
                {
                    "key": "IOS/2019-12-12/2019-09-30T17:00:02.396833/ems-dcounts-stations-small.csv",
                    "csv_valid": True,
                    "csv_rows": 20,
                    "csv_encoding": "utf-8",
                    "ems": "Democracy Counts",
                    "errors": "",
                },
            ],
        }

        upload_serializer = UploadSerializer(data=expected_dict)
        self.assertTrue(upload_serializer.is_valid(raise_exception=True))

        self.assertDictEqual(expected_dict, json.loads(responses.calls[3].request.body))
        resp = self.conn.get_object(
            Bucket=self.final_bucket,
            Key="IOS/2019-12-12/2019-09-30T17:00:02.396833/report.json",
        )
        self.assertEqual(expected_dict, json.loads(resp["Body"].read()))
        ses_backend = ses_backends[moto.core.DEFAULT_ACCOUNT_ID][
            os.environ.get("AWS_DEFAULT_REGION")
        ]
        self.assertEqual(0, len(ses_backend.sent_messages))

    def test_democracy_counts_only_one_file(self):
        self.load_fixture("ems-dcounts-stations.csv", "ems-dcounts-stations.csv")

        main(trigger_payload, None)

        self.assertEqual(2, len(responses.calls))
        self.assertEqual(
            "https://wheredoivote.co.uk/api/beta/uploads/",
            responses.calls[1].request.url,
        )
        expected_dict = {
            "github_issue": "",
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "election_date": "2019-12-12",
            "timestamp": "2019-09-30T17:00:02.396833",
            "file_set": [
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/ems-dcounts-stations.csv",
                    "csv_valid": False,
                    "csv_rows": 20,
                    "csv_encoding": "utf-8",
                    "ems": "Democracy Counts",
                    "errors": "Expected 2 files, found 1",
                }
            ],
        }

        upload_serializer = UploadSerializer(data=expected_dict)
        self.assertTrue(upload_serializer.is_valid(raise_exception=True))

        self.assertDictEqual(expected_dict, json.loads(responses.calls[1].request.body))
        with self.assertRaises(ClientError):
            self.conn.get_object(
                Bucket=self.final_bucket,
                Key="X01000000/2019-09-30T17:00:02.396833/report.json",
            )
        ses_backend = ses_backends[moto.core.DEFAULT_ACCOUNT_ID][
            os.environ.get("AWS_DEFAULT_REGION")
        ]
        self.assertEqual(0, len(ses_backend.sent_messages))

    def test_invalid_one_file(self):
        os.environ["SERVER_ENVIRONMENT"] = "production"
        self.load_fixture("incomplete-file.CSV")

        main(trigger_payload, None)

        self.assertEqual(2, len(responses.calls))
        self.assertEqual(
            "https://wheredoivote.co.uk/api/beta/uploads/",
            responses.calls[1].request.url,
        )
        expected_dict = {
            "github_issue": "",
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "timestamp": "2019-09-30T17:00:02.396833",
            "election_date": "2019-12-12",
            "file_set": [
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/data.csv",
                    "csv_valid": False,
                    "csv_rows": 10,
                    "csv_encoding": "utf-8",
                    "ems": "Xpress DC",
                    "errors": "Incomplete file: Expected 38 columns on row 10 found 7",
                }
            ],
        }

        upload_serializer = UploadSerializer(data=expected_dict)
        self.assertTrue(upload_serializer.is_valid(raise_exception=True))

        self.assertDictEqual(expected_dict, json.loads(responses.calls[1].request.body))
        with self.assertRaises(ClientError):
            self.conn.get_object(
                Bucket=self.final_bucket,
                Key="X01000000/2019-12-12/2019-09-30T17:00:02.396833/report.json",
            )
        ses_backend = ses_backends[moto.core.DEFAULT_ACCOUNT_ID][
            os.environ.get("AWS_DEFAULT_REGION")
        ]
        self.assertEqual(1, len(ses_backend.sent_messages))
        self.assertEqual(
            "Error with data for council X01000000-Piddleton Parish Council",
            ses_backend.sent_messages[0].subject,
        )

    def test_valid_excel_mimetype(self):
        self.load_fixture("ems-idox-eros.csv", mimetype="application/vnd.ms-excel")

        main(trigger_payload, None)

        self.assertEqual(4, len(responses.calls))
        self.assertEqual(
            f"https://api.github.com/repos/{self.repo}/issues",
            responses.calls[2].request.url,
        )
        self.assertEqual(
            "https://wheredoivote.co.uk/api/beta/uploads/",
            responses.calls[3].request.url,
        )
        expected_dict = {
            "github_issue": f"https://github.com/{self.repo}/issues/1",
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "election_date": "2019-12-12",
            "timestamp": "2019-09-30T17:00:02.396833",
            "file_set": [
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/data.csv",
                    "csv_valid": True,
                    "csv_rows": 10,
                    "csv_encoding": "utf-8",
                    "ems": "Idox Eros (Halarose)",
                    "errors": "",
                }
            ],
        }

        upload_serializer = UploadSerializer(data=expected_dict)
        self.assertTrue(upload_serializer.is_valid(raise_exception=True))

        self.assertDictEqual(expected_dict, json.loads(responses.calls[3].request.body))
        resp = self.conn.get_object(
            Bucket=self.final_bucket,
            Key="X01000000/2019-12-12/2019-09-30T17:00:02.396833/report.json",
        )
        self.assertEqual(expected_dict, json.loads(resp["Body"].read()))
        ses_backend = ses_backends[moto.core.DEFAULT_ACCOUNT_ID][
            os.environ.get("AWS_DEFAULT_REGION")
        ]
        self.assertEqual(0, len(ses_backend.sent_messages))
