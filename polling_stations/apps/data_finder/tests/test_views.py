from django.test import TestCase


class HomeViewTestCase(TestCase):
    fixtures = ["test_routing.json"]

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)

    def test_redirect(self):
        response = self.client.post(
            r"/?utm_source=foo&something=other", {"postcode": "AA11AA"}, follow=False
        )
        self.assertEqual(302, response.status_code)
        # The query string isn't preserved, because they've come from the home page, and it could be either slug
        # for the postcode given (hence the [12])
        self.assertRegex(response["Location"], r"/address/[12]/")


class PostCodeViewTestCase(TestCase):
    fixtures = ["test_routing.json"]

    def test_redirect_if_should_be_other_view(self):
        # This should go to the address picker, because it's split over multiple polling districts
        response = self.client.get(
            "/postcode/BB11BB/?utm_source=foo&something=other", follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(response["Location"], "/address_select/BB11BB/?utm_source=foo")


class MultipleCouncilsViewTestCase(TestCase):
    fixtures = ["test_routing.json"]

    def test_redirect_if_should_be_other_view(self):
        # This should go to the address page, because it's actually entirely within one council and polling district
        response = self.client.get(
            "/multiple_councils/AA11AA/?utm_source=foo&something=other", follow=False
        )
        self.assertEqual(302, response.status_code)
        self.assertRegex(response["Location"], r"/address/[12]/\?utm_source=foo")
