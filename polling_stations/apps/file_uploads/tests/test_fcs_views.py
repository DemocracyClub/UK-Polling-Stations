from unittest import mock

from councils.tests.factories import CouncilFactory
from django.contrib.auth.models import User
from file_uploads.models import FcsCredential
from django.test import TestCase
from django.urls import reverse


class FcsViewTestCase(TestCase):
    def setUp(self):
        self.council = CouncilFactory(council_id="ABC")
        self.staff_user = User.objects.create_user(
            username="staff", password="password"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.non_staff_user = User.objects.create_user(
            username="non_staff", password="password"
        )


class TestFcsDateSelectView(FcsViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            "file_uploads:fcs_date_select",
            kwargs={"council_id": self.council.council_id},
        )

    def patch_upcoming_election_dates(self, dates):
        return mock.patch(
            "file_uploads.fcs_views.FcsDateSelectView.get_upcoming_election_dates",
            return_value=dates,
        )

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("file_uploads:council_login_view"), response.url)

    def test_non_staff_user(self):
        self.client.force_login(self.non_staff_user)
        with self.patch_upcoming_election_dates(["2024-05-02"]):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_single_upcoming_date(self):
        self.client.force_login(self.staff_user)
        with self.patch_upcoming_election_dates(["2024-05-02"]):
            response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(
                "file_uploads:fcs_election_select",
                kwargs={
                    "council_id": self.council.council_id,
                    "date": "2024-05-02",
                },
            ),
            fetch_redirect_response=False,
        )

    def test_multiple_upcoming_dates(self):
        self.client.force_login(self.staff_user)
        with self.patch_upcoming_election_dates(["2024-05-02", "2024-06-06"]):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "file_uploads/fcs/date_select.html")
        self.assertContains(response, "2024-05-02")
        self.assertContains(response, "2024-06-06")

    def test_valid_post(self):
        self.client.force_login(self.staff_user)
        with self.patch_upcoming_election_dates(["2024-05-02", "2024-06-06"]):
            response = self.client.post(self.url, {"election_date": "2024-05-02"})
        self.assertRedirects(
            response,
            reverse(
                "file_uploads:fcs_election_select",
                kwargs={
                    "council_id": self.council.council_id,
                    "date": "2024-05-02",
                },
            ),
            fetch_redirect_response=False,
        )

    def test_invalid_post(self):
        self.client.force_login(self.staff_user)
        with self.patch_upcoming_election_dates(["2024-05-02", "2024-06-06"]):
            response = self.client.post(self.url, {"election_date": "not-a-real-date"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "file_uploads/fcs/date_select.html")
        self.assertTrue(response.context["form"].errors)


class TestFcsElectionSelectView(FcsViewTestCase):
    def setUp(self):
        super().setUp()
        self.date = "2024-05-02"
        self.url = reverse(
            "file_uploads:fcs_election_select",
            kwargs={"council_id": self.council.council_id, "date": self.date},
        )
        FcsCredential.objects.create(
            council=self.council,
            url="https://example.com",
            token="fake-token",
        )

    def patch_elections_for_date(self, elections):
        return mock.patch(
            "file_uploads.fcs_views.FcsElectionSelectView.get_elections_for_date",
            return_value=elections,
        )

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("file_uploads:council_login_view"), response.url)

    def test_non_staff_user(self):
        self.client.force_login(self.non_staff_user)
        elections = [{"id": 1, "name": "Election 1", "electionDate": self.date}]
        with self.patch_elections_for_date(elections):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_single_upcoming_election(self):
        self.client.force_login(self.staff_user)
        elections = [{"id": 1, "name": "Election 1", "electionDate": self.date}]
        with self.patch_elections_for_date(elections):
            response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(
                "file_uploads:fcs_snapshot_data",
                kwargs={
                    "council_id": self.council.council_id,
                    "date": self.date,
                    "election_id": 1,
                },
            ),
            fetch_redirect_response=False,
        )

    def test_date_comparison_is_timezone_aware(self):
        self.client.force_login(self.staff_user)
        isoformat_date_during_bst = "2026-10-07T23:00:00Z"
        election_date = "2026-10-08"
        url = reverse(
            "file_uploads:fcs_election_select",
            kwargs={"council_id": self.council.council_id, "date": election_date},
        )
        mock_resp = mock.Mock(return_value=None)
        mock_resp.json.return_value = [
            {"id": 1, "name": "Election 1", "electionDate": isoformat_date_during_bst}
        ]

        with mock.patch("file_uploads.fcs_views.requests.get", return_value=mock_resp):
            response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse(
                "file_uploads:fcs_snapshot_data",
                kwargs={
                    "council_id": self.council.council_id,
                    "date": election_date,
                    "election_id": 1,
                },
            ),
            fetch_redirect_response=False,
        )

    def test_multiple_upcoming_elections(self):
        self.client.force_login(self.staff_user)
        elections = [
            {"id": 1, "name": "Election 1", "electionDate": self.date},
            {"id": 2, "name": "Election 2", "electionDate": self.date},
        ]
        with self.patch_elections_for_date(elections):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "file_uploads/fcs/election_select.html")
        self.assertContains(response, "Election 1")
        self.assertContains(response, "Election 2")

    def test_valid_post(self):
        self.client.force_login(self.staff_user)
        elections = [
            {"id": 1, "name": "Election 1", "electionDate": self.date},
            {"id": 2, "name": "Election 2", "electionDate": self.date},
        ]
        with self.patch_elections_for_date(elections):
            response = self.client.post(self.url, {"election_id": 1})
        self.assertRedirects(
            response,
            reverse(
                "file_uploads:fcs_snapshot_data",
                kwargs={
                    "council_id": self.council.council_id,
                    "date": self.date,
                    "election_id": 1,
                },
            ),
            fetch_redirect_response=False,
        )

    def test_invalid_post(self):
        self.client.force_login(self.staff_user)
        elections = [
            {"id": 1, "name": "Election 1", "electionDate": self.date},
            {"id": 2, "name": "Election 2", "electionDate": self.date},
        ]
        with self.patch_elections_for_date(elections):
            response = self.client.post(self.url, {"election_id": "not-a-real-id"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "file_uploads/fcs/election_select.html")
        self.assertTrue(response.context["form"].errors)


class TestFcsSnapshotDataView(FcsViewTestCase):
    def setUp(self):
        super().setUp()

        self.fcscredential = FcsCredential.objects.create(
            council=self.council,
            url="https://example.com",
            token="fake-token",
        )

        self.date = "2024-05-02"
        self.election_id = "123"
        self.url = reverse(
            "file_uploads:fcs_snapshot_data",
            kwargs={
                "council_id": self.council.council_id,
                "date": self.date,
                "election_id": self.election_id,
            },
        )

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("file_uploads:council_login_view"), response.url)

    def test_non_staff_user(self):
        self.client.force_login(self.non_staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_valid_post(self):
        self.client.force_login(self.staff_user)

        with mock.patch("file_uploads.fcs_views.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = '{"data": "some data"}'
            with mock.patch("file_uploads.fcs_views.boto3.client") as mock_client:
                response = self.client.post(self.url)

                mock_client.return_value.put_object.assert_called_once_with(
                    Bucket="pollingstations.uploads.development",  # default
                    Key=mock.ANY,
                    Body='{"data": "some data"}',
                )

        self.assertEqual(
            self.council.upload_set.all().filter(election_date=self.date).count(), 1
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse(
                "file_uploads:councils_detail", kwargs={"pk": self.council.council_id}
            ),
            response.url,
        )
