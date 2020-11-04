from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geos import Point
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.views import APIView
from api.postcode import PostcodeViewSet
from data_finder.helpers import PostcodeError
from .mocks import EEMockWithElection, EEMockWithoutElection


class StubGeocoder:
    def __init__(self, centroid, code):
        self.centroid = centroid
        self.code = code

    def get_code(self, codetype):
        if not self.code:
            raise ObjectDoesNotExist
        return self.code


"""
Test double for geocode function
allows us to use fake postcodes and return known
results that work with the data in our test fixtures
"""


def mock_geocode(postcode):
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

    # geocoding errors
    if postcode == "FF11FF":
        raise PostcodeError("oh noes!!")

    if postcode == "FOOBAR":
        raise PostcodeError("oh noes!!")


class PostcodeTest(APITestCase):
    fixtures = ["polling_stations/apps/api/fixtures/test_address_postcode.json"]

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get("/foo", format="json")
        self.request.user = AnonymousUser()
        self.request = APIView().initialize_request(self.request)
        self.endpoint = PostcodeViewSet()
        self.endpoint.get_ee_wrapper = lambda x: EEMockWithElection()

    def test_address_list(self):
        response = self.endpoint.retrieve(
            self.request, "AA11AA", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("X01000001", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual(3, len(response.data["addresses"]))
        self.assertIsNone(response.data["custom_finder"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_not_found(self):
        response = self.endpoint.retrieve(
            self.request, "BB11BB", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("X01000002", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual([], response.data["addresses"])
        self.assertIsNone(response.data["custom_finder"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_found(self):
        response = self.endpoint.retrieve(
            self.request, "CC11CC", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("X01000001", response.data["council"]["council_id"])
        self.assertTrue(response.data["polling_station_known"])
        self.assertEqual(
            "St Foo's Church Hall, Bar Town",
            response.data["polling_station"]["properties"]["address"],
        )
        self.assertEqual([], response.data["addresses"])
        self.assertIsNone(response.data["custom_finder"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_found_but_no_election(self):
        self.endpoint.get_ee_wrapper = lambda x: EEMockWithoutElection()
        response = self.endpoint.retrieve(
            self.request, "CC11CC", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("X01000001", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual([], response.data["addresses"])
        self.assertIsNone(response.data["custom_finder"])
        self.assertIsInstance(response.data["postcode_location"], dict)
        self.assertEqual(0, len(response.data["ballots"]))

    def test_station_found_no_source_point(self):
        response = self.endpoint.retrieve(
            self.request, "FF11FF", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("X01000001", response.data["council"]["council_id"])
        self.assertEqual(
            "St Foo's Church Hall, Bar Town",
            response.data["polling_station"]["properties"]["address"],
        )
        self.assertEqual([], response.data["addresses"])
        self.assertIsNone(response.data["custom_finder"])
        self.assertIsNone(response.data["postcode_location"])
        self.assertEqual(1, len(response.data["ballots"]))

    def test_no_council(self):
        response = self.endpoint.retrieve(
            self.request, "DD11DD", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(500, response.status_code)

    def test_bad_postcode(self):
        response = self.endpoint.retrieve(
            self.request, "FOOBAR", "json", geocoder=mock_geocode, log=False
        )

        self.assertEqual(400, response.status_code)

    def test_blacklist(self):
        response = self.endpoint.retrieve(
            self.request, "EE11EE", "json", geocoder=mock_geocode, log=False
        )
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.data["council"])
        self.assertFalse(response.data["polling_station_known"])

    def test_blacklist_lowercase_postcode(self):
        response = self.endpoint.retrieve(
            self.request, "ee11ee", "json", geocoder=mock_geocode, log=False
        )
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.data["council"])
        self.assertFalse(response.data["polling_station_known"])

    def test_cors_header(self):
        resp = self.client.get(
            "/api/postcode/AA11AA/", format="json", HTTP_ORIGIN="foo.bar/baz"
        )
        self.assertEqual(resp.get("Access-Control-Allow-Origin"), "*")
