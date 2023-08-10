from unittest import mock

import pytest
from councils.models import Council, UserCouncils
from django.contrib.auth.models import User
from django.test import TestCase
from file_uploads.utils import assign_councils_to_user

TEST_CUSTOM_DOMAINS = {
    "custom_council.gov.uk": ["ABD", "ABE"],
    "another_custom_council.gov.uk": ["ALL"],
}


class TestCustomDomainEmailCheck(TestCase):
    def setUp(self):
        Council.objects.create(
            council_id="ABD",
            electoral_services_email="bob@not_custom_council.gov.uk",
            registration_email="bob@not_custom_council.gov.uk",
        )
        Council.objects.create(
            council_id="ABE",
            electoral_services_email="bob@not_custom_council.gov.uk",
            registration_email="bob@not_custom_council.gov.uk",
        )
        Council.objects.create(
            council_id="ALL",
            electoral_services_email="bob@council.gov.uk",
            registration_email="bob@council.gov.uk",
        )

    @pytest.mark.django_db
    @mock.patch("file_uploads.utils.CUSTOM_DOMAINS", TEST_CUSTOM_DOMAINS)
    def test_assign_approved_custom_domains(self, custom_domains=TEST_CUSTOM_DOMAINS):
        user = User.objects.create(email="james@custom_council.gov.uk")
        assign_councils_to_user(user)
        self.assertEqual(user.council_set.count(), 2)
        self.assertEqual(user.council_set.all()[0].council_id, "ABD")
        self.assertEqual(user.council_set.all()[1].council_id, "ABE")
        self.assertFalse(
            UserCouncils.objects.filter(user=user, council__council_id="ALL").exists()
        )

    @pytest.mark.django_db
    @mock.patch("file_uploads.utils.CUSTOM_DOMAINS", TEST_CUSTOM_DOMAINS)
    def test_standard_domains(self, custom_domains=TEST_CUSTOM_DOMAINS):
        user = User.objects.create(email="james@not_custom_council.gov.uk")
        assign_councils_to_user(user)
        self.assertEqual(user.council_set.count(), 2)
        self.assertTrue(
            UserCouncils.objects.filter(user=user, council__council_id="ABD").exists()
        )
        self.assertTrue(
            UserCouncils.objects.filter(user=user, council__council_id="ABE").exists()
        )
        self.assertFalse(
            UserCouncils.objects.filter(user=user, council__council_id="ALL").exists()
        )

    @pytest.mark.django_db
    @mock.patch("file_uploads.utils.CUSTOM_DOMAINS", TEST_CUSTOM_DOMAINS)
    def test_login_for_user_with_multiple_councils_assigned(self):
        user = User.objects.create(email="james@custom_council.gov.uk")
        assign_councils_to_user(user)
        self.assertEqual(user.council_set.count(), 2)

        self.client.force_login(user)
        response = self.client.get("/uploads/councils/")
        self.assertTrue(response.status_code, 200)
        # response contains a list of councils
        self.assertContains(response, "ABD")
        self.assertContains(response, "ABE")
        self.assertNotContains(response, "ALL")
