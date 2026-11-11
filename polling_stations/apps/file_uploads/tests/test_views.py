from datetime import timedelta

from councils.tests.factories import CouncilFactory
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from file_uploads.tests.factories import FileFactory, UploadFactory


class TestCouncilListView(TestCase):
    def setUp(self):
        self.url = reverse("file_uploads:councils_list")
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.client.force_login(self.staff_user)

    def create_council_with_valid_future_upload(self, council_id):
        council = CouncilFactory(council_id=council_id)
        upload = UploadFactory(
            gss=council,
            election_date=timezone.now().date() + timedelta(days=7),
        )
        FileFactory(upload=upload, csv_valid=True)
        return council

    def test_shows_status_of_latest_future_upload(self):
        self.create_council_with_valid_future_upload("AAA")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        # The council has no polling stations, so the only tick on the
        # page is the upload status.
        self.assertContains(response, "✔️")

    def test_query_count_does_not_grow_with_number_of_councils(self):
        """
        The upload status of each council comes from an annotation on the
        council queryset. Looking it up per row in the template instead
        costs one query per council, which made this page take over a
        second for staff users, who see every council.
        """
        for i in range(10):
            self.create_council_with_valid_future_upload(f"X{i:02}")

        # 1. user
        # 2. count of councils (CouncilListView.get)
        # 3. councils, annotated with upload status and station count
        with self.assertNumQueries(3):
            response = self.client.get(self.url)

        self.assertEqual(len(response.context["object_list"]), 10)
