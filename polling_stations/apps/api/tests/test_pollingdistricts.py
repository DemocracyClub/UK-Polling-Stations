from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.pollingdistricts import PollingDistrictViewSet

class PollingDistrictsTest(TestCase):
    fixtures = ['polling_stations/apps/api/fixtures/test_api_pollingdistricts_stations.json']

    def test_bad_request(self):
        # passing a district_id param with no council_id param should throw
        # 400 Bad Request
        factory = APIRequestFactory()
        request = factory.get(
            '/foo?district_id=FOO', format='json')
        response = PollingDistrictViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(400, response.status_code)

    def test_unknown_council(self):
        # council that matches no districts should return empty array []
        factory = APIRequestFactory()
        request = factory.get(
            '/foo?council_id=X01000002', format='json')
        response = PollingDistrictViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_valid_council(self):
        factory = APIRequestFactory()
        request = factory.get(
            '/foo?council_id=X01000001', format='json')
        response = PollingDistrictViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.data))

    def test_valid_council_geo(self):
        factory = APIRequestFactory()
        request = factory.get(
            '/foo?council_id=X01000001', format='json')
        response = PollingDistrictViewSet.as_view({'get': 'geo'})(request)
        self.assertEqual(200, response.status_code)
        # geo response should be a FeatureCollection, not an array
        self.assertEqual('FeatureCollection', response.data['type'])
        self.assertEqual(3, len(response.data['features']))

    def test_district_with_valid_station(self):
        factory = APIRequestFactory()
        request = factory.get(
            '/foo?council_id=X01000001&district_id=AA', format='json')
        response = PollingDistrictViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('AA', response.data['district_id'])
        self.assertEqual(
            "St Foo's Church Hall, Bar Town",
            response.data['polling_station']['address']
        )

    def test_district_with_null_station(self):
        factory = APIRequestFactory()
        request = factory.get(
            '/foo?council_id=X01000001&district_id=CC', format='json')
        response = PollingDistrictViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('CC', response.data['district_id'])
        self.assertEqual(None, response.data['polling_station'])

    def test_district_geo(self):
        factory = APIRequestFactory()

        # set up geojson request for district X01000001.AA
        geo_request = factory.get(
            '/foo?council_id=X01000001&district_id=AA', format='json')
        geo_response = PollingDistrictViewSet.as_view({'get': 'geo'})(geo_request)

        # set up json request for district X01000001.AA
        request = factory.get(
            '/foo?council_id=X01000001&district_id=AA', format='json')
        response = PollingDistrictViewSet.as_view({'get': 'list'})(request)

        # geo_response should contain geometry
        self.assertEqual(True, ('geometry' in geo_response.data))
        self.assertEqual('MultiPolygon', geo_response.data['geometry']['type'])

        # (non-geo) response should not contain gemoetry
        self.assertEqual(True, ('geometry' not in response.data))

        # properties key of geo_response should be the same as (non-geo) response
        self.assertEqual(response.data, geo_response.data['properties'])

        self.assertEqual('AA', response.data['district_id'])
