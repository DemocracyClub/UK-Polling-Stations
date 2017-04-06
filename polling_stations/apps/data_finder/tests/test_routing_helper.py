from django.test import TestCase
from addressbase.models import Blacklist
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

    def test_multiple_councils_view(self):
        # check we are directed to multiple_councils_view if
        # postcode is attached to multiple councils in the blacklist
        rh = RoutingHelper('DD11DD')
        endpoint = rh.get_endpoint()
        self.assertEqual('multiple_councils_view', endpoint.view)

    def test_multiple_councils_view_override(self):
        # insert blacklist records for postcodes matching other conditions
        Blacklist.objects.create(postcode='AA11AA', lad='X01000001')
        Blacklist.objects.create(postcode='AA11AA', lad='W06000022')
        Blacklist.objects.create(postcode='BB11BB', lad='X01000001')
        Blacklist.objects.create(postcode='BB11BB', lad='W06000022')
        Blacklist.objects.create(postcode='CC11CC', lad='X01000001')
        Blacklist.objects.create(postcode='CC11CC', lad='W06000022')

        # check the blacklist overrides all other conditions
        rh = RoutingHelper('AA11AA')
        endpoint = rh.get_endpoint()
        self.assertEqual('multiple_councils_view', endpoint.view)

        rh = RoutingHelper('BB11BB')
        endpoint = rh.get_endpoint()
        self.assertEqual('multiple_councils_view', endpoint.view)

        rh = RoutingHelper('CC11CC')
        endpoint = rh.get_endpoint()
        self.assertEqual('multiple_councils_view', endpoint.view)
