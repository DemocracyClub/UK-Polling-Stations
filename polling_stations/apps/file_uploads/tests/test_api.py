from django.core.management import call_command
from rest_framework.test import APITestCase

from councils.tests.factories import CouncilFactory
from file_uploads.models import File, Upload


class AddressTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01000001",
            name="Piddleton Parish Council",
            identifiers=["X01000001"],
            geography__geography=None,
        )

        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/file_uploads/fixtures/test_api.json",
            verbosity=0,
        )

    def test_invalid_payload(self):
        invalid_payloads = [
            {},  # empty object
            {"gss": "X01000001"},  # missing fields
            {
                "gss": "X01000002",  # invalid GSS code
                "timestamp": "2020-01-10T13:26:05Z",
                "github_issue": "",
                "file_set": [],
            },
            {
                "gss": "X01000001",
                "timestamp": "2020-01-10T13:26:05Z",
                "github_issue": "",
                "file_set": [
                    {
                        "csv_valid": "ello dave",  # wrong type (should be a bool)
                        "csv_rows": 25432,
                        "ems": "Xpress DC",
                        "errors": "Incomplete file: Expected 38 columns on row 25432 found 7",
                        "key": "E07000223/2020-01-10T15:38:59.029979/richmondshire-Democracy_Club__02May2019.CSV",
                    }
                ],
            },
        ]
        for payload in invalid_payloads:
            self.client.credentials(HTTP_AUTHORIZATION="Token superuser-key")
            resp = self.client.post("/api/beta/uploads/", payload, format="json")
            self.assertEqual(400, resp.status_code)  # Bad Request
            self.assertEqual(0, len(Upload.objects.all()))
            self.assertEqual(0, len(File.objects.all()))

    def test_get_request(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token superuser-key")
        resp = self.client.get("/api/beta/uploads/")
        self.assertEqual(405, resp.status_code)  # Method Not Allowed
        self.assertEqual(0, len(Upload.objects.all()))
        self.assertEqual(0, len(File.objects.all()))

    def test_valid_payload_no_auth(self):
        payload = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [],
        }
        resp = self.client.post("/api/beta/uploads/", payload, format="json")
        self.assertEqual(401, resp.status_code)  # Unauthorized
        self.assertEqual(0, len(Upload.objects.all()))
        self.assertEqual(0, len(File.objects.all()))

    def test_valid_payload_bad_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token normaluser-key")
        payload = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [],
        }
        resp = self.client.post("/api/beta/uploads/", payload, format="json")
        self.assertEqual(403, resp.status_code)  # Forbidden
        self.assertEqual(0, len(Upload.objects.all()))
        self.assertEqual(0, len(File.objects.all()))

    def test_valid_payload_zero_files(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token superuser-key")
        payload = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [],
        }
        resp = self.client.post("/api/beta/uploads/", payload, format="json")
        self.assertEqual(201, resp.status_code)
        self.assertEqual(1, len(Upload.objects.all()))
        self.assertEqual(0, len(File.objects.all()))

    def test_valid_payload_one_file(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token superuser-key")
        payload = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [
                {
                    "csv_valid": False,
                    "csv_rows": 25432,
                    "ems": "Xpress DC",
                    "errors": "Incomplete file: Expected 38 columns on row 25432 found 7",
                    "key": "E07000223/2020-01-10T15:38:59.029979/richmondshire-Democracy_Club__02May2019.CSV",
                }
            ],
        }
        resp = self.client.post("/api/beta/uploads/", payload, format="json")
        self.assertEqual(201, resp.status_code)
        self.assertEqual(1, len(Upload.objects.all()))
        self.assertEqual(1, len(File.objects.all()))

    def test_valid_payload_two_files(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token superuser-key")
        payload = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [
                {
                    "csv_valid": True,
                    "csv_rows": 86109,
                    "ems": "Democracy Counts",
                    "errors": "",
                    "key": "E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Districts.csv",
                },
                {
                    "csv_valid": True,
                    "csv_rows": 69,
                    "ems": "Democracy Counts",
                    "errors": "",
                    "key": "E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Stations.csv",
                },
            ],
        }
        resp = self.client.post("/api/beta/uploads/", payload, format="json")
        self.assertEqual(201, resp.status_code)
        self.assertEqual(1, len(Upload.objects.all()))
        self.assertEqual(2, len(File.objects.all()))

    def test_multiple_files_out_of_order_delivery(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token superuser-key")

        # The first payload we receive for this upload contains 2 files
        payload1 = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [
                {
                    "csv_valid": True,
                    "csv_rows": 86109,
                    "ems": "Democracy Counts",
                    "errors": "",
                    "key": "E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Districts.csv",
                },
                {
                    "csv_valid": True,
                    "csv_rows": 69,
                    "ems": "Democracy Counts",
                    "errors": "",
                    "key": "E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Stations.csv",
                },
            ],
        }
        resp = self.client.post("/api/beta/uploads/", payload1, format="json")
        self.assertEqual(201, resp.status_code)
        # assert we've inserted it correctly
        self.assertEqual(1, len(Upload.objects.all()))
        self.assertEqual(2, len(File.objects.all()))
        stations_file = File.objects.get(
            key="E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Stations.csv"
        )
        self.assertEqual("", stations_file.errors)

        # The second payload we receive only contains one of the files
        # that was in the first payload.
        # This upload was actually processed first, but we're receiving it
        # later because an out-of-order delivery has happened.
        payload2 = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [
                {
                    "csv_valid": True,
                    "csv_rows": 69,
                    "ems": "Democracy Counts",
                    "errors": "Expected 2 files, found 1",
                    "key": "E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Stations.csv",
                },
            ],
        }
        resp = self.client.post("/api/beta/uploads/", payload2, format="json")
        self.assertEqual(201, resp.status_code)
        self.assertEqual(1, len(Upload.objects.all()))
        # we should still have 2 file objects attached to this upload, not 1
        self.assertEqual(2, len(File.objects.all()))
        # stations_file.errors should still be "", not "Expected 2 files, found 1"
        stations_file = File.objects.get(
            key="E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Stations.csv"
        )
        self.assertEqual("", stations_file.errors)

        payload3 = {
            "gss": "X01000001",
            "timestamp": "2020-01-10T13:26:05Z",
            "github_issue": "",
            "file_set": [
                {
                    "csv_valid": True,
                    "csv_rows": 86109,
                    "ems": "Democracy Counts",
                    "errors": "",
                    "key": "E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Districts.csv",
                },
                {
                    "csv_valid": True,
                    "csv_rows": 69,
                    "ems": "Democracy Counts",
                    "errors": "",
                    "key": "E07000223/2020-01-10T15:38:21.962203/luton-DC - Polling Stations.csv",
                },
                {
                    "csv_valid": True,
                    "csv_rows": 100,
                    "ems": "Democracy Counts",
                    "errors": "",
                    "key": "E07000223/2020-01-10T15:38:21.962203/some other file.csv",
                },
            ],
        }
        resp = self.client.post("/api/beta/uploads/", payload3, format="json")
        self.assertEqual(201, resp.status_code)
        self.assertEqual(1, len(Upload.objects.all()))
        # now we should have 3 file objects
        self.assertEqual(3, len(File.objects.all()))
