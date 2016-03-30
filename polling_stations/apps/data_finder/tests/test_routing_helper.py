from django.test import TestCase
from data_finder.helpers import RoutingHelper

class RoutingHelperTest(TestCase):

    fixtures = ['test_routing.json']

    def test_address_view(self):
        rh = RoutingHelper()
        endpoint = rh.get_endpoint('AA11AA')
        self.assertEqual('address_view', endpoint.view)

    def test_address_select_view(self):
        rh = RoutingHelper()
        endpoint = rh.get_endpoint('BB11BB')
        self.assertEqual('address_select_view', endpoint.view)

    def test_postcode_view(self):
        rh = RoutingHelper()
        endpoint = rh.get_endpoint('CC11CC')
        self.assertEqual('postcode_view', endpoint.view)
