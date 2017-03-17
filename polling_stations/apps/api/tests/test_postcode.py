from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.postcode import PostcodeViewSet


"""
Test double for geocode function
allows us to use fake postcodes and return known
results that work with the data in our test fixtures
"""
def mock_geocode(postcode):
    # list of addresses
    if (postcode == 'AA11AA'):
        return {
            'wgs84_lon': 0.22247314453125,
            'wgs84_lat': 53.149405955929744,
            'gss_codes': [],
        }

    # council with no data
    if (postcode == 'BB11BB'):
        return {
            'wgs84_lon': -3.54583740234375,
            'wgs84_lat': 52.019712234868464,
            'gss_codes': [],
        }

    # polling station 1
    if (postcode == 'CC11CC'):
        return {
            'wgs84_lon': -2.1533203125,
            'wgs84_lat': 52.858517622387716,
            'gss_codes': [],
        }

    # no council
    if (postcode == 'DD11DD'):
        return {
            'wgs84_lon': -4.6142578125,
            'wgs84_lat': 57.45913526799062,
            'gss_codes': [],
        }

    # Northern Ireland
    if (postcode == 'BT11AA'):
        return {
            'wgs84_lon': -6.7950439453125,
            'wgs84_lat': 54.746820492190885,
            'gss_codes': ['N07000001'],
        }


class PostcodeTest(TestCase):
    fixtures = [
        'polling_stations/apps/api/fixtures/test_address_postcode.json',
        'polling_stations/apps/data_finder/fixtures/northern_ireland.json',
    ]

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get('/foo', format='json')
        self.endpoint = PostcodeViewSet()

    def test_address_list(self):
        response = self.endpoint.retrieve(self.request, 'AA11AA', 'json',
            geocoder=mock_geocode, log=False)

        self.assertEqual(200, response.status_code)
        self.assertEqual('X01000001', response.data['council']['council_id'])
        self.assertFalse(response.data['polling_station_known'])
        self.assertEqual(None, response.data['polling_station'])
        self.assertEqual(3, len(response.data['addresses']))
        self.assertIsNone(response.data['custom_finder'])

    def test_station_not_found(self):
        response = self.endpoint.retrieve(self.request, 'BB11BB', 'json',
            geocoder=mock_geocode, log=False)

        self.assertEqual(200, response.status_code)
        self.assertEqual('X01000002', response.data['council']['council_id'])
        self.assertFalse(response.data['polling_station_known'])
        self.assertEqual(None, response.data['polling_station'])
        self.assertEqual([], response.data['addresses'])
        self.assertIsNone(response.data['custom_finder'])

    def test_station_found(self):
        response = self.endpoint.retrieve(self.request, 'CC11CC', 'json',
            geocoder=mock_geocode, log=False)

        self.assertEqual(200, response.status_code)
        self.assertEqual('X01000001', response.data['council']['council_id'])
        self.assertTrue(response.data['polling_station_known'])
        self.assertEqual("St Foo's Church Hall, Bar Town",
            response.data['polling_station']['properties']['address'])
        self.assertEqual([], response.data['addresses'])
        self.assertIsNone(response.data['custom_finder'])

    def test_no_council(self):
        response = self.endpoint.retrieve(self.request, 'DD11DD', 'json',
            geocoder=mock_geocode, log=False)

        self.assertEqual(500, response.status_code)

    def test_northern_ireland(self):
        response = self.endpoint.retrieve(self.request, 'BT11AA', 'json',
            geocoder=mock_geocode, log=False)

        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.data['council'])
        self.assertFalse(response.data['polling_station_known'])
        self.assertIsNone(response.data['polling_station'])
        self.assertEqual([], response.data['addresses'])
        self.assertEqual(
            "http://www.eoni.org.uk/Offices/Postcode-Search-Results?postcode=BT1%201AA",
            response.data['custom_finder']
        )
