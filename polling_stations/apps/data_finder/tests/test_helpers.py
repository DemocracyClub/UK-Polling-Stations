from django.test import TestCase, override_settings
from data_finder.helpers import ExamplePostcodeHelper

@override_settings(EXAMPLE_POSTCODE='CF10 5AJ')
class ExamplePostcodeTest(TestCase):
    def setUp(self):
        self.example_postcode = ExamplePostcodeHelper()

    def test_example_postcode_display(self):
        assert self.example_postcode.display == "CF10 5AJ"

    def test_example_postcode_url(self):
        assert self.example_postcode.url == "/postcode/CF105AJ/"

    def test_example_postcode_context(self):
        resp = self.client.get('/')
        assert 'example_postcode' in resp.context
        assert resp.context['example_postcode'].display == "CF10 5AJ"

