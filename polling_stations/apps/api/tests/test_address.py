from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geos import Point
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from api.address import AddressViewSet
from councils.tests.factories import CouncilFactory
from .mocks import EEMockWithElection, EEMockWithoutElection


# Test double for geocode function: always returns the same point
def mock_geocode(postcode):
    return type(
        "Geocoder",
        (object,),
        {"centroid": Point(0.22247314453125, 53.149405955929744, srid=4326)},
    )


class AddressTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="ABC",
            identifiers=["X01000001"],
            geography__geography="MULTIPOLYGON (((-2.83447265625 53.64203274279828,1.549072265625 53.64203274279828,1.549072265625 52.52691653862567,-2.83447265625 52.52691653862567,-2.83447265625 53.64203274279828)))",
        )
        CouncilFactory(
            council_id="DEF",
            identifiers=["X01000002"],
            geography__geography="MULTIPOLYGON (((-4.141845703125 52.20491365416633,-2.8125 52.20491365416633,-2.8125 51.731111030918306,-4.141845703125 51.731111030918306,-4.141845703125 52.20491365416633)))",
        )
        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/api/fixtures/test_address_postcode.json",
            verbosity=0,
        )

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get("/foo", format="json")
        self.request.user = AnonymousUser()
        self.request = APIView().initialize_request(self.request)
        self.endpoint = AddressViewSet()
        self.endpoint.get_ee_wrapper = lambda x: EEMockWithElection()

    def test_station_found(self):
        response = self.endpoint.retrieve(
            self.request,
            "200",
            "json",
            geocoder=mock_geocode,
            log=False,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertTrue(response.data["polling_station_known"])
        self.assertEqual(
            "Foo Street Primary School, Bar Town",
            response.data["polling_station"]["properties"]["address"],
        )
        self.assertEqual(1, len(response.data["addresses"]))
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_found_but_no_election(self):
        self.endpoint.get_ee_wrapper = lambda x: EEMockWithoutElection()
        response = self.endpoint.retrieve(
            self.request,
            "200",
            "json",
            geocoder=mock_geocode,
            log=False,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual(1, len(response.data["addresses"]))
        self.assertEqual(0, len(response.data["ballots"]))

    def test_station_not_found(self):
        response = self.endpoint.retrieve(
            self.request,
            "202",
            "json",
            geocoder=mock_geocode,
            log=False,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual(1, len(response.data["addresses"]))
        self.assertEqual(1, len(response.data["ballots"]))

    def test_bad_slug(self):
        # this address is not in our fixture
        response = self.endpoint.retrieve(
            self.request,
            "205",
            "json",
            geocoder=mock_geocode,
            log=False,
        )

        self.assertEqual(404, response.status_code)
