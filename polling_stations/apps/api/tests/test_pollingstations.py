from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.pollingstations import PollingStationViewSet


class PollingStationsTest(TestCase):
    fixtures = [
        "polling_stations/apps/api/fixtures/test_api_pollingdistricts_stations.json"
    ]

    def test_bad_request(self):
        # passing a station_id param with no council_id param should throw
        # 400 Bad Request
        factory = APIRequestFactory()
        request = factory.get("/foo?station_id=FOO", format="json")
        response = PollingStationViewSet.as_view({"get": "list"})(request)
        self.assertEqual(400, response.status_code)

    def test_unknown_council(self):
        # council that matches no stations should return empty array []
        factory = APIRequestFactory()
        request = factory.get("/foo?council_id=X01000003", format="json")
        response = PollingStationViewSet.as_view({"get": "list"})(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_valid_council(self):
        factory = APIRequestFactory()
        request = factory.get("/foo?council_id=X01000001", format="json")
        response = PollingStationViewSet.as_view({"get": "list"})(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))

    def test_valid_council_geo(self):
        factory = APIRequestFactory()
        request = factory.get("/foo?council_id=X01000001", format="json")
        response = PollingStationViewSet.as_view({"get": "geo"})(request)
        self.assertEqual(200, response.status_code)
        # geo response should be a FeatureCollection, not an array
        self.assertEqual("FeatureCollection", response.data["type"])
        self.assertEqual(2, len(response.data["features"]))

    def test_station_geo(self):
        factory = APIRequestFactory()

        # set up geojson request for station X01000001.1
        geo_request = factory.get(
            "/foo?council_id=X01000001&station_id=1", format="json"
        )
        geo_response = PollingStationViewSet.as_view({"get": "geo"})(geo_request)

        # set up json request for station X01000001.1
        request = factory.get("/foo?council_id=X01000001&station_id=1", format="json")
        response = PollingStationViewSet.as_view({"get": "list"})(request)

        # geo_response should contain geometry
        self.assertEqual(True, ("geometry" in geo_response.data))
        self.assertEqual("Point", geo_response.data["geometry"]["type"])

        # (non-geo) response should not contain gemoetry
        self.assertEqual(True, ("geometry" not in response.data))

        # properties key of geo_response should be the same as (non-geo) response
        self.assertEqual(response.data, geo_response.data["properties"])

        self.assertEqual("St Foo's Church Hall, Bar Town", response.data["address"])

    def test_null_point(self):
        factory = APIRequestFactory()
        request = factory.get("/foo?council_id=X01000001&station_id=2", format="json")
        response = PollingStationViewSet.as_view({"get": "geo"})(request)

        self.assertEqual(None, response.data["geometry"])
