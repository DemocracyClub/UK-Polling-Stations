import datetime

from api.postcode import PostcodeViewSet
from councils.tests.factories import CouncilFactory
from data_finder.helpers import PostcodeError, RoutingHelper
from data_importers.event_types import DataEventType
from data_importers.tests.factories import DataEventFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.views import APIView
from uk_geo_utils.helpers import Postcode
from unittest.mock import patch

from .mocks import EEMockWithElection, EEMockWithoutElection


class StubGeocoder:
    def __init__(self, centroid, code):
        self.centroid = centroid
        self.code = code

    def get_code(self, codetype):
        if not self.code:
            raise ObjectDoesNotExist
        return self.code


def mock_geocode(postcode):
    """
    Test double for geocode function
    allows us to use fake postcodes and return known
    results that work with the data in our test fixtures
    """
    postcode = postcode.without_space
    # list of addresses
    if postcode == "AA11AA":
        return StubGeocoder(
            Point(0.22247314453125, 53.149405955929744, srid=4326), "X01000001"
        )

    # council with no data
    if postcode == "BB11BB":
        return StubGeocoder(
            Point(-3.54583740234375, 52.019712234868464, srid=4326), "X01000002"
        )

    # polling station 1
    if postcode == "CC11CC":
        return StubGeocoder(
            Point(-2.1533203125, 52.858517622387716, srid=4326), "X01000001"
        )

    # no council
    if postcode == "DD11DD":
        return StubGeocoder(Point(-4.6142578125, 57.45913526799062, srid=4326), None)

    if postcode == "FOOBAR":
        raise PostcodeError("oh noes!!")
    return None


class PostcodeTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="ABC",
            identifiers=["X01000001"],
            geography__geography="MULTIPOLYGON (((-2.83447265625 53.64203274279828,1.549072265625 53.64203274279828,1.549072265625 52.52691653862567,-2.83447265625 52.52691653862567,-2.83447265625 53.64203274279828)))",
        )
        DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.IMPORT,
            created=timezone.now() - datetime.timedelta(days=7),
            election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
            metadata={
                "test info": "Import for future election",
                "Imported": "7 days ago",
            },
        )
        CouncilFactory(
            council_id="DEF",
            identifiers=["X01000002"],
            geography__geography="MULTIPOLYGON (((-4.141845703125 52.20491365416633,-2.8125 52.20491365416633,-2.8125 51.731111030918306,-4.141845703125 51.731111030918306,-4.141845703125 52.20491365416633)))",
        )
        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/api/fixtures/test_address_postcode.json",
            verbosity=0,
        )

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get(
            "/foo", format="json", headers={"Authorization": "Token test_token"}
        )
        self.request.user = AnonymousUser()
        self.request = APIView().initialize_request(self.request)
        self.endpoint = PostcodeViewSet()
        self.endpoint.get_ee_wrapper = lambda x, rh, params: EEMockWithElection()

    def test_address_list(self):
        response = self.endpoint.retrieve(
            self.request, "AA11AA", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual(3, len(response.data["addresses"]))
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_not_found(self):
        response = self.endpoint.retrieve(
            self.request, "BB11BB", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("DEF", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertTrue("advance_voting_station" in response.data)
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual([], response.data["addresses"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_found(self):
        response = self.endpoint.retrieve(
            self.request, "CC11CC", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertTrue(response.data["polling_station_known"])
        self.assertEqual(
            "St Foo's Church Hall, Bar Town",
            response.data["polling_station"]["properties"]["address"],
        )
        self.assertEqual([], response.data["addresses"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(1, len(response.data["ballots"]))
        self.assertTrue("requires_voter_id" in response.data["ballots"][0])

    def test_station_found_but_no_election(self):
        self.endpoint.get_ee_wrapper = lambda x, rh, params: EEMockWithoutElection()
        response = self.endpoint.retrieve(
            self.request, "CC11CC", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual([], response.data["addresses"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(0, len(response.data["ballots"]))

    def test_station_found_with_election_but_data_event_for_past_election(self):
        DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.IMPORT,
            created=timezone.now() - datetime.timedelta(days=3),
            election_dates=[timezone.now().date() - datetime.timedelta(days=1)],
            metadata={
                "test info": "Import for previous election",
                "Imported": "3 days ago",
            },
        )
        response = self.endpoint.retrieve(
            self.request, "CC11CC", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual([], response.data["addresses"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(1, len(response.data["ballots"]))

    def test_no_council(self):
        with self.assertRaises(APIException):
            self.endpoint.retrieve(
                self.request, "DD11DD", "json", geocoder=mock_geocode, log=False
            )

    def test_bad_postcode(self):
        response = self.endpoint.retrieve(
            self.request, "FOOBAR", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(400, response.status_code)

    def test_cors_header(self):
        resp = self.client.get(
            "/api/postcode/AA11AA/", format="json", HTTP_ORIGIN="foo.bar/baz"
        )
        self.assertEqual(resp.get("Access-Control-Allow-Origin"), "*")


class GetEEWrapperTest(TestCase):
    def setUp(self):
        self.endpoint = PostcodeViewSet()
        self.query_params = {}

    def test_success_parquet(self):
        postcode = "AA11AA"
        rh = RoutingHelper(Postcode(postcode))
        setattr(rh, "_elections_response", {"request_success": True, "ballots": []})
        ee_wrapper = self.endpoint.get_ee_wrapper(postcode, rh, self.query_params)
        self.assertTrue(ee_wrapper.request_success)

    def test_fail_parquet(self):
        postcode = "AA11AA"
        rh = RoutingHelper(Postcode(postcode))
        setattr(rh, "_elections_response", {"request_success": False})
        with self.assertRaises(APIException):
            self.endpoint.get_ee_wrapper(postcode, rh, self.query_params)

    @patch("api.postcode.EEFetcher.fetch")
    def test_success_live(self, mock_fetch):
        mock_fetch.return_value = {"request_success": True, "elections": []}
        postcode = "AA11AA"
        rh = RoutingHelper(Postcode(postcode))
        ee_wrapper = self.endpoint.get_ee_wrapper(postcode, rh, self.query_params)
        self.assertTrue(ee_wrapper.request_success)

    @patch("api.postcode.EEFetcher.fetch")
    def test_fail_live(self, mock_fetch):
        mock_fetch.return_value = {"request_success": False}
        postcode = "AA11AA"
        rh = RoutingHelper(Postcode(postcode))
        with self.assertRaises(APIException):
            self.endpoint.get_ee_wrapper(postcode, rh, self.query_params)
