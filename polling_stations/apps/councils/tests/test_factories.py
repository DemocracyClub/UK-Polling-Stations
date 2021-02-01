from django.test import TestCase

from councils.models import CouncilGeography
from councils.tests.factories import CouncilFactory


class TestCouncilFactory(TestCase):
    def test_council_factory(self):
        council = CouncilFactory()
        self.assertEqual(len(council.council_id), 3)
        self.assertIsInstance(council.geography, CouncilGeography)
