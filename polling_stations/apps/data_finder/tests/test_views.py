from django.core.management import call_command
from django.test import TestCase

from councils.tests.factories import CouncilFactory


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


class PostCodeViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            identifiers=["X01"],
            geography__geography=None,
        )

        for fixture in ["test_routing.json", "test_multiple_polling_stations.json"]:
            call_command(  # Hack to avoid converting all fixtures to factories
                "loaddata",
                fixture,
                verbosity=0,
            )

    def test_redirect_if_should_be_other_view(self):
        # This should go to the address picker, because it's split over multiple polling districts
        response = self.client.get(
            "/postcode/DD11DD/?utm_source=foo&something=other", follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], "/address_select/DD11DD/?utm_source=foo")


class PostCodeViewNoStationTestCase(TestCase):
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

    def test_polling_station_is_blank(self):
        response = self.client.get(
            "/postcode/BB11BB/?utm_source=foo&something=other", follow=False
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Contact Foo Council")
        self.assertContains(response, "tel:01314 159265")

    def test_post_code_not_in_addressbase(self):
        response = self.client.get(
            "/postcode/HJ67KL/?utm_source=foo&something=other", follow=False
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Contact Foo Council")
        self.assertContains(response, "tel:01314 159265")


class WeDontknowViewTestCase(TestCase):
    """
    'FF22FF' is a postcode with uprns in multiple councils and some polling stations.
    'GG22GG' is a postcode with uprns in multiple councils and no polling stations.
    'HH22HH' is a postcode with uprns in a single council and no polling stations.
    """

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
        response = self.client.get("/we_dont_know/FF22FF/", follow=False)

        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], r"/multiple_councils/FF22FF/")

    def test_multiple_councils_view(self):
        response = self.client.get("/multiple_councils/FF22FF/", follow=False)
        self.assertContains(
            response,
            "Residents in FF22FF may be in one of the following council areas:",
        )
        self.assertContains(response, "Foo Council")
        self.assertContains(response, "Bar Borough")

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
        response = self.client.get("/multiple_councils/GG22GG/", follow=False)
        self.assertContains(
            response,
            "Residents in GG22GG may be in one of the following council areas:",
        )
        self.assertContains(response, "Foo Council")
        self.assertContains(response, "Bar Borough")
