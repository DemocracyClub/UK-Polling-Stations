import json

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from councils.models import Council
from councils.tests.factories import CouncilFactory
from pollingstations.models import PollingStation

"""
Tests for the dashboard

Mostly just to test the views raise no exceptions, as opposed to testing the results they produce.
"""

UserModel = get_user_model()


class DashboardTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="FOO",
            name="Foo Council",
            identifiers=["X01"],
            geography__geography=None,
        )
        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/dashboard/fixtures/test_dashboard.json",
            verbosity=0,
        )

    def setUp(self):
        self.user = UserModel.objects.create(username="staff", is_staff=True)
        self.client.force_login(self.user)


class CouncilDetailViewTestCase(DashboardTestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="FOO",
            name="Foo Council",
            identifiers=["X01"],
            geography__geography=None,
        )
        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/dashboard/fixtures/test_dashboard.json",
            verbosity=0,
        )

    def test_get(self):
        council = Council.objects.get(pk="FOO")
        response = self.client.get("/dashboard/council/{}/".format(council.pk))
        self.assertEqual(200, response.status_code)
        self.assertEqual(council, response.context["council"])


class PostCodeViewTestCase(DashboardTestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="FOO",
            name="Foo Council",
            identifiers=["X01"],
            geography__geography=None,
        )
        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/dashboard/fixtures/test_dashboard.json",
            verbosity=0,
        )

    def test_known_postcode(self):
        response = self.client.get("/dashboard/postcode/AA11AA/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context["addresses"]))


class PostCodeGeoJSONTestCase(DashboardTestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="FOO",
            name="Foo Council",
            identifiers=["X01"],
            geography__geography=None,
        )
        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/dashboard/fixtures/test_dashboard.json",
            verbosity=0,
        )

    def test_unknown_postcode(self):
        response = self.client.get("/dashboard/postcode/ZZ11ZZ.geojson")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/geo+json", response["Content-Type"])
        self.assertEqual("application/geo+json", response["Content-Type"])
        self.assertEqual(
            {"type": "FeatureCollection", "features": []}, json.loads(response.content)
        )

    def test_known_postcode(self):
        response = self.client.get("/dashboard/postcode/DD11DD.geojson")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/geo+json", response["Content-Type"])
        data = json.loads(response.content)
        self.assertEqual("FeatureCollection", data["type"])
        self.assertEqual(
            2,
            len(
                [
                    feature
                    for feature in data["features"]
                    if feature["properties"]["type"] == "pollingstation"
                ]
            ),
        )
        self.assertEqual(
            3,
            len(
                [
                    feature
                    for feature in data["features"]
                    if feature["properties"]["type"] == "residentialaddress"
                ]
            ),
        )


class PollingStationDetailView(DashboardTestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="FOO",
            name="Foo Council",
            identifiers=["X01"],
            geography__geography=None,
        )
        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/dashboard/fixtures/test_dashboard.json",
            verbosity=0,
        )

    def test_get(self):
        polling_station = PollingStation.objects.get(pk=1)
        response = self.client.get(
            "/dashboard/council/{}/polling-station/{}/".format(
                polling_station.council_id, polling_station.internal_council_id
            )
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(polling_station, response.context["pollingstation"])
