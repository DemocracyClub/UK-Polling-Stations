from django.test import TestCase


class HomeViewTestCase(TestCase):
    fixtures = [
        "test_routing.json",
        "test_multiple_addresses_single_polling_station.json",
    ]

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
    fixtures = ["test_routing.json", "test_multiple_polling_stations.json"]

    def test_redirect_if_should_be_other_view(self):
        # This should go to the address picker, because it's split over multiple polling districts
        response = self.client.get(
            "/postcode/DD11DD/?utm_source=foo&something=other", follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], "/address_select/DD11DD/?utm_source=foo")
