from django.test import TestCase

from councils.models import Council
from councils.tests.factories import CouncilFactory


class CouncilTest(TestCase):
    def setUp(self):

        CouncilFactory(
            **{
                "council_id": "NWP",
                "electoral_services_address": "Newport City Council\nCivic Centre\nNewport\nSouth Wales",
                "electoral_services_email": "uvote@newport.gov.uk",
                "electoral_services_phone_numbers": ["01633 656656"],
                "electoral_services_postcode": "NP20 4UR",
                "electoral_services_website": "http://www.newport.gov.uk/_dc/index.cfm?fuseaction=electoral.homepage",
                "name": "Newport Council",
                "identifiers": ["W06000022"],
            }
        )

    def test_nation(self):
        newport = Council.objects.get(pk="NWP")
        self.assertEqual("Wales", newport.nation)
