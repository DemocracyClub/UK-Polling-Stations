import datetime
from unittest.mock import patch

from addressbase.models import Address
from addressbase.tests.factories import AddressFactory, UprnToCouncilFactory
from councils.tests.factories import CouncilFactory
from data_finder.views import (
    AddressView,
    get_date_context,
    polling_station_current,
    reverse_with_qs,
)
from data_importers.event_types import DataEventType
from data_importers.tests.factories import DataEventFactory
from django.core.management import call_command
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone
from pollingstations.models import PollingStation, VisibilityChoices
from pollingstations.tests.factories import PollingStationFactory
from uk_geo_utils.helpers import Postcode
from zoneinfo import ZoneInfo
from django.http import QueryDict
from unittest import mock


class LogTestMixin:
    @override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": False})
    def test_dc_logging(self):
        with self.assertLogs(level="DEBUG") as captured:
            self.client.get(
                f"/postcode/{self.test_dc_logging_postcode}/",
                {
                    "foo": "bar",
                    "utm_source": "test",
                    "utm_campaign": "better_tracking",
                    "utm_medium": "pytest",
                },
                HTTP_AUTHORIZATION="Token foo",
                follow=True,
            )

        for record in captured.records:
            if record.message.startswith("dc-postcode-searches"):
                logging_message = record

        assert logging_message

        assert (
            f'"postcode": "{self.test_dc_logging_postcode}"' in logging_message.message
        )
        assert '"dc_product": "WDIV"' in logging_message.message
        assert '"had_election": false' in logging_message.message
        assert '"utm_source": "test"' in logging_message.message
        assert '"utm_campaign": "better_tracking"' in logging_message.message
        assert '"utm_medium": "pytest"' in logging_message.message


class TestReverseWithQs(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            identifiers=["X01"],
            geography__geography=None,
        )

        call_command(
            "loaddata",
            "test_multiple_addresses_single_polling_station.json",
            verbosity=0,
        )

    def test_reverse_with_qs(self):
        request = mock.Mock()
        request.GET = QueryDict("utm_source=foo&something=other")
        self.assertEqual(
            reverse_with_qs("address_view", {"uprn": "102"}, request),
            "/address/102/?utm_source=foo",
        )


class HomeViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            identifiers=["X01"],
            geography__geography=None,
        )

        for fixture in [
            "test_routing.json",
            "test_multiple_addresses_single_polling_station.json",
        ]:
            call_command(  # Hack to avoid converting all fixtures to factories
                "loaddata",
                fixture,
                verbosity=0,
            )

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)

    def test_redirect(self):
        response = self.client.post(
            r"/?utm_source=foo&something=other", {"postcode": "CC1 1AA"}, follow=False
        )
        self.assertEqual(302, response.status_code)
        # The query string isn't preserved, because they've come from the home page, and it could be either uprn
        # for the postcode given (hence the [23])
        self.assertRegex(response["Location"], r"/address/10[23]/")

    def test_get_date_context(self):
        self.assertDictEqual({"show_polls_open_card": False}, get_date_context(None))

        six_am_election_day = datetime.datetime(
            2024, 5, 2, 6, tzinfo=ZoneInfo("Europe/London")
        )
        midday_election_day = datetime.datetime(
            2024, 5, 2, 12, tzinfo=ZoneInfo("Europe/London")
        )
        after_polls_close_election_day = datetime.datetime(
            2024, 5, 2, 22, 10, tzinfo=ZoneInfo("Europe/London")
        )

        with patch.object(timezone, "now", return_value=six_am_election_day):
            self.assertDictEqual(
                {
                    "election_date": datetime.datetime(
                        2024, 5, 2, 0, 0, tzinfo=ZoneInfo(key="Europe/London")
                    ),
                    "election_date_is_today": True,
                    "show_polls_open_card": True,
                },
                get_date_context("2024-05-02"),
            )
        with patch.object(timezone, "now", return_value=midday_election_day):
            self.assertDictEqual(
                {
                    "election_date": datetime.datetime(
                        2024, 5, 2, 0, 0, tzinfo=ZoneInfo(key="Europe/London")
                    ),
                    "election_date_is_today": True,
                    "show_polls_open_card": True,
                },
                get_date_context("2024-05-02"),
            )
        with patch.object(timezone, "now", return_value=after_polls_close_election_day):
            self.assertDictEqual(
                {
                    "election_date": datetime.datetime(
                        2024, 5, 2, 0, 0, tzinfo=ZoneInfo(key="Europe/London")
                    ),
                    "election_date_is_today": True,
                    "show_polls_open_card": False,
                },
                get_date_context("2024-05-02"),
            )


class PostCodeViewTestCase(TestCase, LogTestMixin):
    test_dc_logging_postcode = "AA11AA"

    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            identifiers=["X01"],
            geography__geography=None,
        )
        DataEventFactory(
            council_id="X01",
            event_type=DataEventType.IMPORT,
            election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
        )

        for fixture in [
            "test_routing.json",
            "test_multiple_polling_stations.json",
            "test_single_address_single_polling_station.json",
        ]:
            call_command(  # Hack to avoid converting all fixtures to factories
                "loaddata",
                fixture,
                verbosity=0,
            )

    def test_redirect_if_should_be_other_view(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            # This should go to the address picker, because it's split over multiple polling districts
            response = self.client.get(
                "/postcode/DD11DD/?utm_source=foo&something=other", follow=False
            )
            self.assertEqual(302, response.status_code)
            self.assertEqual(
                response["Location"], "/address_select/DD11DD/?utm_source=foo"
            )

            # shouldn't log because follow=False
            mock_log.assert_not_called()

    def test_station_known(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            response = self.client.get(
                "/postcode/AA11AA/?utm_source=foo&something=other", follow=False
            )
            self.assertEqual(302, response.status_code)
            self.assertEqual(response["Location"], "/address/100/?utm_source=foo")

            # shouldn't log because follow=False
            mock_log.assert_not_called()

    def test_log_postcode_called(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            self.client.get(
                "/postcode/AA11AA/", follow=True
            )  # follow=True because we want to log the search at the point the user sees a result

            # Should log because we show a result
            mock_log.assert_called_once()

    def test_log_postcode_not_called_on_redirect(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            self.client.get(
                "/postcode/DD11DD/", follow=True
            )  # follow=True because we want to log the search at the point the user sees a result

            # shouldn't log because we redirect to AddressSelectForm
            mock_log.assert_not_called()


class AddressViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            identifiers=["X01"],
            geography__geography=None,
        )
        DataEventFactory(
            council_id="X01",
            event_type=DataEventType.IMPORT,
            election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
        )
        for fixture in [
            "test_single_address_single_polling_station.json",
            "test_single_address_blank_polling_station.json",
        ]:
            call_command(  # Hack to avoid converting all fixtures to factories
                "loaddata",
                fixture,
                verbosity=0,
            )

    def setUp(self):
        self.factory = RequestFactory()

    def test_station_known_response(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            response = self.client.get("/address/100/", follow=False)
            self.assertEqual(200, response.status_code)

            # Should log because we show a result
            mock_log.assert_called_once()

    def test_get_station_station_known(self):
        request = self.factory.get("/address/100/")
        view = AddressView()
        view.setup(request)
        view.address = Address.objects.select_related("uprntocouncil").get(uprn="100")
        view.postcode = Postcode("AA11AA")
        context = view.get_context_data()
        self.assertTrue(context["we_know_where_you_should_vote"])
        self.assertEqual(context["station"].internal_council_id, "1A")

    def test_get_station_station_unknown(self):
        request = self.factory.get("/address/101/")
        view = AddressView()
        view.setup(request)
        view.address = Address.objects.select_related("uprntocouncil").get(uprn="101")
        view.postcode = Postcode("BB11BB")
        context = view.get_context_data()
        self.assertFalse(context["we_know_where_you_should_vote"])
        self.assertIsNone(context["station"])

    def test_get_station_station_known_unpublished(self):
        PollingStationFactory(
            council_id="X01",
            internal_council_id="BAD",
            visibility=VisibilityChoices.UNPUBLISHED,
        )
        address = AddressFactory(uprn="1234", postcode="TE1 1ST")
        UprnToCouncilFactory(
            uprn=address,
            lad="X01",
        )
        request = self.factory.get("/address/1234/")
        view = AddressView()
        view.setup(request)
        view.address = Address.objects.select_related("uprntocouncil").get(uprn="1234")
        view.postcode = Postcode("TE11ST")
        context = view.get_context_data()
        self.assertFalse(context["we_know_where_you_should_vote"])
        self.assertIsNone(context["station"])

    @override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": True})
    def test_log_postcode_has_election_true(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            self.client.get("/address/100/", follow=False)

            # Verify log_postcode was called
            mock_log.assert_called_once()

            # Check the context passed to log_postcode
            call_args = mock_log.call_args
            context = call_args[0][1]  # Second argument is context
            self.assertTrue(context["has_election"])

    @override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": False})
    def test_log_postcode_has_election_false(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            self.client.get("/address/100/", follow=False)

            # Verify log_postcode was called
            mock_log.assert_called_once()

            # Check the context passed to log_postcode
            call_args = mock_log.call_args
            context = call_args[0][1]  # Second argument is context
            self.assertFalse(context["has_election"])


class PostCodeViewNoStationTestCase(TestCase, LogTestMixin):
    test_dc_logging_postcode = "BB11BB"

    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            name="Foo Council",
            electoral_services_phone_numbers=["01314 159265"],
            identifiers=["X01"],
            geography__geography=None,
        )

        for fixture in [
            "test_single_address_blank_polling_station.json",
            "test_postcode_not_in_addressbase.json",
        ]:
            call_command(  # Hack to avoid converting all fixtures to factories
                "loaddata",
                fixture,
                verbosity=0,
            )

    @override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": False})
    def test_polling_station_is_blank(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            response = self.client.get(
                "/postcode/BB11BB/?utm_source=foo&something=other", follow=False
            )
            self.assertEqual(200, response.status_code)
            self.assertContains(response, "ontact Foo Council")
            self.assertContains(response, "tel:01314 159265")

            # Should log because we show a result
            mock_log.assert_called_once()

    def test_post_code_not_in_addressbase(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            response = self.client.get(
                "/postcode/HJ67KL/?utm_source=foo&something=other", follow=False
            )
            self.assertEqual(200, response.status_code)
            self.assertContains(response, "Contact Foo Council")
            self.assertContains(response, "tel:01314 159265")

            # Should log because we show a result
            mock_log.assert_called_once()


class WeDontknowViewTestCase(TestCase):
    """
    'FF22FF' is a postcode with uprns in multiple councils and some polling stations.
    'GG22GG' is a postcode with uprns in multiple councils and no polling stations.
    'HH22HH' is a postcode with uprns in a single council and no polling stations.
    """

    def test_dc_logging(self):
        # This test case is for when user's address isn't in the list and the postcode
        # is split over multiple councils.
        with self.assertLogs(level="DEBUG") as captured:
            self.client.get(
                "/multiple_councils/FF22FF/",
                {
                    "foo": "bar",
                    "utm_source": "test",
                    "utm_campaign": "better_tracking",
                    "utm_medium": "pytest",
                },
                HTTP_AUTHORIZATION="Token foo",
                follow=True,
            )

        for record in captured.records:
            if record.message.startswith("dc-postcode-searches"):
                logging_message = record

        assert logging_message

        assert '"postcode": "FF22FF"' in logging_message.message
        assert '"dc_product": "WDIV"' in logging_message.message
        assert '"had_election": false' in logging_message.message
        assert '"utm_source": "test"' in logging_message.message
        assert '"utm_campaign": "better_tracking"' in logging_message.message
        assert '"utm_medium": "pytest"' in logging_message.message

    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="FOO",
            name="Foo Council",
            identifiers=["X01"],
            geography__geography=None,
        )
        CouncilFactory(
            council_id="BAR",
            name="Bar Borough",
            identifiers=["X02"],
            geography__geography=None,
        )

        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "test_uprns_in_multiple_councils",
            verbosity=0,
        )

    def test_not_multiple_redirect(self):
        response = self.client.post(
            r"/?utm_source=foo&something=other", {"postcode": "HH2 2HH"}, follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], r"/postcode/HH22HH/")

    def test_home_redirect(self):
        response = self.client.post(
            r"/?utm_source=foo&something=other", {"postcode": "FF2 2FF"}, follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], r"/address_select/FF22FF/")

    def test_we_dont_know_redirect(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            response = self.client.get("/we_dont_know/FF22FF/", follow=False)

            self.assertEqual(302, response.status_code)
            self.assertEqual(response["Location"], r"/multiple_councils/FF22FF/")

            # Shouldn't log because follow=False
            mock_log.assert_not_called()

    def test_multiple_councils_view(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            response = self.client.get("/multiple_councils/FF22FF/", follow=False)
            self.assertContains(
                response,
                "Residents in FF22FF may be in one of the following council areas:",
            )
            self.assertContains(response, "Foo Council")
            self.assertContains(response, "Bar Borough")

            # Should log because we show a result
            mock_log.assert_called_once()

    def test_home_redirect_no_stations(self):
        response = self.client.post(
            r"/?utm_source=foo&something=other", {"postcode": "GG2 2GG"}, follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], r"/address_select/GG22GG/")

    def test_postcode_redirect_no_stations(self):
        response = self.client.get("/postcode/GG22GG/", follow=False)
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], r"/address_select/GG22GG/")

    def test_multiple_councils_no_stations(self):
        with patch("data_finder.views.LogLookUpMixin.log_postcode") as mock_log:
            response = self.client.get("/multiple_councils/GG22GG/", follow=False)
            self.assertContains(
                response,
                "Residents in GG22GG may be in one of the following council areas:",
            )
            self.assertContains(response, "Foo Council")
            self.assertContains(response, "Bar Borough")

            # Should log because we show a result
            mock_log.assert_called_once()


class PollingStationCurrentTestCase(TestCase):
    def setUp(self):
        self.council = CouncilFactory()
        self.station = PollingStationFactory(council=self.council)
        self.uprn = UprnToCouncilFactory(
            lad=self.council.geography.gss,
            polling_station_id=self.station.internal_council_id,
        )

    def test_station_is_current_future_election(self):
        DataEventFactory(
            council=self.council,
            event_type=DataEventType.IMPORT,
            created=timezone.now() - datetime.timedelta(days=3),
            election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
        )
        self.assertTrue(
            polling_station_current(self.uprn.uprn.polling_station_with_elections())
        )

    def test_station_is_current_today_election(self):
        DataEventFactory(
            council=self.council,
            event_type=DataEventType.IMPORT,
            created=timezone.now() - datetime.timedelta(days=3),
            election_dates=[timezone.now().date()],
        )
        self.assertTrue(
            polling_station_current(self.uprn.uprn.polling_station_with_elections())
        )

    def test_station_is_not_current_past_election(self):
        DataEventFactory(
            council=self.council,
            event_type=DataEventType.IMPORT,
            created=timezone.now() - datetime.timedelta(days=3),
            election_dates=[timezone.now().date() - datetime.timedelta(days=1)],
        )
        self.assertFalse(
            polling_station_current(self.uprn.uprn.polling_station_with_elections())
        )

    def test_station_elections_are_strings_not_dates(self):
        """This shouldn't happen because the db field on DataEvent is an array of dates"""
        ps = PollingStation.objects.all().first()
        ps.elections = ["foo"]
        self.assertFalse(polling_station_current(ps))

    def test_station_has_no_elections_attribute(self):
        ps = PollingStation.objects.all().first()
        self.assertFalse(polling_station_current(ps))
