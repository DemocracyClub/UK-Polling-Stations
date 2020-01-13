from rest_framework.test import APITestCase
from file_uploads.models import File, Upload


class AddressTest(APITestCase):
    fixtures = ["polling_stations/apps/file_uploads/fixtures/test_api.json"]

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
