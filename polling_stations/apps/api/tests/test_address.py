import datetime

from addressbase.models import Address
from api.address import AddressViewSet
from councils.tests.factories import CouncilFactory
from data_importers.event_types import DataEventType
from data_importers.tests.factories import DataEventFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.test import override_settings, TestCase
from django.utils import timezone
from pollingstations.models import PollingStation, VisibilityChoices
from rest_framework.exceptions import APIException
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from unittest.mock import patch

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
        DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.IMPORT,
            created=timezone.now() - datetime.timedelta(days=7),
            election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
            metadata={
                "test info": "Import for future election",
                "Imported": "7 days ago",
            },
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
        self.request = factory.get(
            "/foo", format="json", headers={"Authorization": "Token test_token"}
        )
        self.request.user = AnonymousUser()
        self.request = APIView().initialize_request(self.request)
        self.endpoint = AddressViewSet()
        self.endpoint.get_ee_wrapper = lambda x, params: EEMockWithElection()

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
        self.assertTrue("advance_voting_station" in response.data)
        self.assertEqual(
            "Foo Street Primary School, Bar Town",
            response.data["polling_station"]["properties"]["address"],
        )
        self.assertEqual(1, len(response.data["addresses"]))
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_exists_but_is_unpublished_with_election(self):
        # Unpublish the station
        ps = PollingStation.objects.get(council_id="ABC", internal_council_id="2")
        ps.visibility = VisibilityChoices.UNPUBLISHED
        ps.save()

        # Do the request
        response = self.endpoint.retrieve(
            self.request,
            "200",
            "json",
            geocoder=mock_geocode,
            log=False,
        )

        # Check nothing found
        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertFalse(response.data["polling_station_known"])
        self.assertEqual(None, response.data["polling_station"])
        self.assertEqual(1, len(response.data["addresses"]))
        self.assertEqual(1, len(response.data["ballots"]))

        # Republish the station
        ps.visibility = VisibilityChoices.PUBLISHED
        ps.save()

        # Redo the request
        response = self.endpoint.retrieve(
            self.request,
            "200",
            "json",
            geocoder=mock_geocode,
            log=False,
        )

        # Check something is found
        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council"]["council_id"])
        self.assertTrue(response.data["polling_station_known"])
        self.assertTrue("advance_voting_station" in response.data)
        self.assertEqual(
            "Foo Street Primary School, Bar Town",
            response.data["polling_station"]["properties"]["address"],
        )
        self.assertEqual(1, len(response.data["addresses"]))
        self.assertEqual(1, len(response.data["ballots"]))

    def test_station_found_but_no_election(self):
        self.endpoint.get_ee_wrapper = lambda x, params: EEMockWithoutElection()
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

    def test_station_found_with_election_but_data_event_for_past_election(self):
        DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.IMPORT,
            created=timezone.now() - datetime.timedelta(days=3),
            election_dates=[timezone.now().date() - datetime.timedelta(days=1)],
            metadata={
                "test info": "Import for previous election",
                "Imported": "3 days ago",
            },
        )
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
        self.assertEqual(1, len(response.data["ballots"]))

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


class GetEEWrapperTest(TestCase):
    def setUp(self):
        self.viewset = AddressViewSet()
        self.address = Address(
            uprn="100080051217",
            postcode="AB1 2CD",
            location=Point(0.22247314453125, 53.149405955929744, srid=4326),
        )
        self.query_params = {}

    @patch("api.address.LocalParquetElectionsHelper")
    @override_settings(USE_LOCAL_PARQUET_ELECTIONS=True)
    def test_success_parquet(self, MockHelper):
        mock_helper_instance = MockHelper.return_value
        mock_helper_instance.get_response.return_value = {
            "request_success": True,
            "ballots": [],
        }

        ee_wrapper = self.viewset.get_ee_wrapper(self.address, self.query_params)
        self.assertTrue(ee_wrapper.request_success)

    @patch("api.address.LocalParquetElectionsHelper")
    @override_settings(USE_LOCAL_PARQUET_ELECTIONS=True)
    def test_fail_parquet(self, MockHelper):
        mock_helper_instance = MockHelper.return_value
        mock_helper_instance.get_response.return_value = {
            "request_success": False,
        }

        with self.assertRaises(APIException):
            self.viewset.get_ee_wrapper(self.address, self.query_params)

    @patch("api.address.EEFetcher")
    @override_settings(USE_LOCAL_PARQUET_ELECTIONS=False)
    def test_success_live(self, MockFetcher):
        mock_fetcher_instance = MockFetcher.return_value
        mock_fetcher_instance.fetch.return_value = {
            "request_success": True,
            "elections": [],
        }

        ee_wrapper = self.viewset.get_ee_wrapper(self.address, self.query_params)
        self.assertTrue(ee_wrapper.request_success)

    @patch("api.address.EEFetcher")
    @override_settings(USE_LOCAL_PARQUET_ELECTIONS=False)
    def test_fail_live(self, MockFetcher):
        mock_fetcher_instance = MockFetcher.return_value
        mock_fetcher_instance.fetch.return_value = {
            "request_success": False,
        }

        with self.assertRaises(APIException):
            self.viewset.get_ee_wrapper(self.address, self.query_params)
