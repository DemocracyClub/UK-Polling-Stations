import datetime
import json

from data_importers.event_types import DataEventType
from data_importers.tests.factories import DataEventFactory
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from polling_stations.apps.councils.tests.factories import CouncilFactory

"""
Tests for the feedback app

"""


class FeedbackTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            identifiers=["X01"],
            geography__geography=None,
        )
        DataEventFactory(
            council_id="X01",
            event_type=DataEventType.IMPORT,
            election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
        )

        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/data_finder/fixtures/test_single_address_single_polling_station.json",
            verbosity=0,
        )

    @override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": True})
    def test_feedback_form(self):
        response = self.client.get("/postcode/AA11AA", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["we_know_where_you_should_vote"])
        self.assertEqual(response.context["station"].internal_council_id, "1A")
        self.assertTemplateUsed(response, "feedback/feedback_form.html")

        self.feedback_form = response.context["feedback_form"]

        self.assertContains(
            response,
            '<input type="radio" name="found_useful" value="YES" data-toggle="button" required id="id_found_useful_0">',
        )
        self.assertContains(
            response,
            '<input type="radio" name="vote" value="MORE_LIKELY" data-toggle="button" id="id_vote_0" required>',
        )
        self.assertContains(response, "Did you find what you were looking for?")
        self.assertContains(
            response, "Has this service changed your likelihood of voting?"
        )

        request = self.client.post(
            "/feedback/",
            {
                "found_useful": "YES",
                "vote": "MORE_LIKELY",
                "source_url": "/postcode/AA11AA",
                "token": "test_token",
            },
            format=json,
            follow=True,
        )

        self.assertContains(request, "Thank you for your feedback!")
