from unittest import mock

from django.http import QueryDict
from django.test import TestCase
from addressbase.models import Blacklist
from data_finder.helpers import RoutingHelper


class RoutingHelperTest(TestCase):

    fixtures = ["test_routing.json"]

    def test_address_view(self):
        rh = RoutingHelper("AA11AA")
        self.assertEqual("address_view", rh.view)

    def test_address_select_view(self):
        rh = RoutingHelper("BB11BB")
        self.assertEqual("address_select_view", rh.view)

    def test_postcode_view(self):
        rh = RoutingHelper("CC11CC")
        self.assertEqual("postcode_view", rh.view)

    def test_multiple_councils_view(self):
        # check we are directed to multiple_councils_view if
        # postcode is attached to multiple councils in the blacklist
        rh = RoutingHelper("DD11DD")
        self.assertEqual("multiple_councils_view", rh.view)

    def test_multiple_councils_view_override(self):
        # insert blacklist records for postcodes matching other conditions
        Blacklist.objects.create(postcode="AA11AA", lad="X01000001")
        Blacklist.objects.create(postcode="AA11AA", lad="W06000022")
        Blacklist.objects.create(postcode="BB11BB", lad="X01000001")
        Blacklist.objects.create(postcode="BB11BB", lad="W06000022")
        Blacklist.objects.create(postcode="CC11CC", lad="X01000001")
        Blacklist.objects.create(postcode="CC11CC", lad="W06000022")

        # check the blacklist overrides all other conditions
        rh = RoutingHelper("AA11AA")
        self.assertEqual("multiple_councils_view", rh.view)

        rh = RoutingHelper("BB11BB")
        self.assertEqual("multiple_councils_view", rh.view)

        rh = RoutingHelper("CC11CC")
        self.assertEqual("multiple_councils_view", rh.view)

    def test_multiple_councils_lowercase_postcode(self):
        # check we are directed to multiple_councils_view if
        # postcode is attached to multiple councils in the blacklist
        rh = RoutingHelper("dd11dd")
        self.assertEqual("multiple_councils_view", rh.view)

    def test_canonical_url(self):
        rh = RoutingHelper("AA11AA")
        request = mock.Mock()
        request.GET = QueryDict("utm_source=foo&something=other")
        # Could be either slug
        self.assertRegex(
            rh.get_canonical_url(request), "/address/[12]/\?utm_source=foo"
        )

    def test_canonical_url_without_preserve(self):
        rh = RoutingHelper("AA11AA")
        request = mock.Mock()
        request.GET = QueryDict("utm_source=foo&something=other")
        # Could be either slug
        self.assertRegex(
            rh.get_canonical_url(request, preserve_query=False), "/address/[12]/"
        )
