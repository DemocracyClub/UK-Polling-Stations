from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geos import Point
from rest_framework.test import APIRequestFactory
from api.address import ResidentialAddressViewSet
from .mocks import EEMockWithElection, EEMockWithoutElection


# Test double for geocode function: always returns the same point
def mock_geocode(postcode):
    return type(
        "Geocoder", (object, ),
        { "centroid": Point(0.22247314453125, 53.149405955929744, srid=4326) }
    )


class AddressTest(TestCase):
    fixtures = ['polling_stations/apps/api/fixtures/test_address_postcode.json']

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get('/foo', format='json')
        self.request.user = AnonymousUser()
        self.endpoint = ResidentialAddressViewSet()
        self.endpoint.get_ee_wrapper = lambda x: EEMockWithElection()

    def test_station_found(self):
        response = self.endpoint.retrieve(self.request,
            '1-foo-street-bar-town', 'json', geocoder=mock_geocode, log=False)

        self.assertEqual(200, response.status_code)
        self.assertEqual('X01000001', response.data['council']['council_id'])
        self.assertTrue(response.data['polling_station_known'])
        self.assertEqual("Foo Street Primary School, Bar Town",
            response.data['polling_station']['properties']['address'])
        self.assertEqual(1, len(response.data['addresses']))

    def test_station_found_but_no_election(self):
        self.endpoint.get_ee_wrapper = lambda x: EEMockWithoutElection()
        response = self.endpoint.retrieve(self.request,
            '1-foo-street-bar-town', 'json', geocoder=mock_geocode, log=False)

        self.assertEqual(200, response.status_code)
        self.assertEqual('X01000001', response.data['council']['council_id'])
        self.assertFalse(response.data['polling_station_known'])
        self.assertEqual(None, response.data['polling_station'])
        self.assertEqual(1, len(response.data['addresses']))

    def test_station_not_found(self):
        response = self.endpoint.retrieve(self.request,
            '3-foo-street-bar-town', 'json', geocoder=mock_geocode, log=False)

        self.assertEqual(200, response.status_code)
        self.assertEqual('X01000001', response.data['council']['council_id'])
        self.assertFalse(response.data['polling_station_known'])
        self.assertEqual(None, response.data['polling_station'])
        self.assertEqual(1, len(response.data['addresses']))

    def test_bad_slug(self):
        # this address is not in our fixture
        response = self.endpoint.retrieve(self.request,
            '4-foo-street-bar-town', 'json', geocoder=mock_geocode, log=False)

        self.assertEqual(404, response.status_code)
