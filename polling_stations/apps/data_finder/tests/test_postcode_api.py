from django.test import TestCase
from data_finder.helpers import RoutingHelper
from django.core.urlresolvers import reverse

import vcr


class APITests(TestCase):
    """
    SW1A1AA - all addresses have the same polling station
    SW1A2AA - Two different polling stations for this postcode
    """

    fixtures = [
        'test_api.json',
    ]

    @vcr.use_cassette('test_data/vcr_cassettes/test_address_api.yaml')
    def test_address_api_expecting_address_picker(self):
        postcode = 'SW1A2AA'
        url = reverse(
            'postcode-detail',
            kwargs={'pk': postcode}
        )
        res = self.client.get(url)
        self.assertEqual(res.data['response_type'], "multiple_addresses")
        self.assertEqual(res.data['polling_station_known'], False)
        self.assertEqual(len(res.data['addresses']), 2)

    def test_address_api_expecting_polling_station(self):
        postcode = 'SW1A1AA'
        url = reverse(
            'postcode-detail',
            kwargs={'pk': postcode}
        )
        res = self.client.get(url)
        self.assertEqual(res.data['response_type'], "single_address")
        self.assertEqual(res.data['polling_station_known'], True)

    def test_postcode_view(self):
        postcode = 'NP205GN'
        url = reverse(
            'postcode-detail',
            kwargs={'pk': postcode}
        )
        res = self.client.get(url)
        self.assertEqual(res.data['response_type'], "postcode")
        self.assertEqual(res.data['polling_station_known'], True)
