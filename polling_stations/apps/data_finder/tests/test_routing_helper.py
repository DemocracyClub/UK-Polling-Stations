from django.test import TestCase
from data_finder.helpers import RoutingHelper

class RoutingHelperTest(TestCase):

    fixtures = ['test_routing.json']

    def test_address_view(self):
        rh = RoutingHelper('AA11AA')
        endpoint = rh.get_endpoint()
        self.assertEqual('address_view', endpoint.view)

    def test_address_select_view(self):
        rh = RoutingHelper('BB11BB')
        endpoint = rh.get_endpoint()
        self.assertEqual('address_select_view', endpoint.view)

    def test_postcode_view(self):
        rh = RoutingHelper('CC11CC')
        endpoint = rh.get_endpoint()
        self.assertEqual('postcode_view', endpoint.view)
