from django.test import TestCase

from councils.models import Council


class CouncilTest(TestCase):
    fixtures = ["newport_council.json"]

    def test_nation(self):
        newport = Council.objects.get(pk="NWP")
        self.assertEqual("Wales", newport.nation)
