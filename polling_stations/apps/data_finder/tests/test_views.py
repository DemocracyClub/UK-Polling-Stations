from django.test import TestCase
from django.urls import reverse

from data_finder.tests.utils import PostcodeBuilder


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.postcode_unassigned_addresses = (
            PostcodeBuilder().with_unassigned_addresses()
        )
        self.postcode_assigned_addresses = PostcodeBuilder().with_assigned_addresses()
        self.postcode_mixed_addresses = (
            PostcodeBuilder().with_assigned_addresses().with_unassigned_addresses()
        )

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)

    def test_redirect_with_unassigned_addresses(self):
        response = self.client.post(
            reverse("home") + "?utm_source=foo&something=other",
            {"postcode": self.postcode_unassigned_addresses.postcode},
            follow=False,
        )
        self.assertEqual(302, response.status_code)
        self.assertRegex(
            response["location"],
            f"/postcode/{self.postcode_unassigned_addresses.postcode.replace(' ','')}/",
        )

    def test_redirect_with_assigned_addresses(self):
        response = self.client.post(
            reverse("home") + "?utm_source=foo&something=other",
            {"postcode": self.postcode_assigned_addresses.postcode},
            follow=False,
        )
        self.assertEqual(302, response.status_code)
        self.assertRegex(response["location"], "/address/[0-9]{9}/")

    def test_redirect_with_mixed_addresses(self):
        response = self.client.post(
            reverse("home") + "?utm_source=foo&something=other",
            {"postcode": self.postcode_mixed_addresses.postcode},
            follow=False,
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response["location"],
            f"/address_select/{self.postcode_mixed_addresses.postcode.replace(' ','')}/",
        )


class PostCodeViewTestCase(TestCase):
    fixtures = ["test_routing.json", "test_multiple_polling_stations.json"]

    def test_redirect_if_should_be_other_view(self):
        # This should go to the address picker, because it's split over multiple polling districts
        response = self.client.get(
            "/postcode/DD11DD/?utm_source=foo&something=other", follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], "/address_select/DD11DD/?utm_source=foo")


class PostCodeViewNoStationTestCase(TestCase):
    fixtures = [
        "test_single_address_blank_polling_station.json",
        "test_postcode_not_in_addressbase.json",
    ]

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
    fixtures = ["test_uprns_in_multiple_councils"]
    """
    'FF22FF' is a postcode with uprns in multiple councils and some polling stations.
    'GG22GG' is a postcode with uprns in multiple councils and no polling stations.
    'HH22HH' is a postcode with uprns in a single council and no polling stations.
    """

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
