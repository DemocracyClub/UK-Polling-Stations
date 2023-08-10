from addressbase.models import Address, UprnToCouncil
from councils.models import Council
from councils.tests.factories import CouncilFactory
from data_importers.data_types import AssignPollingStationsMixin
from django.test import TestCase


class MockCollection(AssignPollingStationsMixin):
    def __init__(self):
        self.elements = []

    def get_polling_station_lookup(self):
        return {
            "1": {
                "001",
            },
        }


class AssignPollingStationsMixinTest(TestCase):
    def setUp(self):
        CouncilFactory(council_id="Foo", identifiers=["X0100000"])
        Address.objects.update_or_create(pk="001")
        Address.objects.update_or_create(pk="002")
        UprnToCouncil.objects.update_or_create(pk="001", lad="X0100000")
        UprnToCouncil.objects.update_or_create(pk="002", lad="X0100000")
        self.mock_collection = MockCollection()
        self.mock_collection.elements = [{"council": Council.objects.get(pk="Foo")}]

    def test_council_id(self):
        self.assertEqual(self.mock_collection.council_id, "Foo")

    def test_gss_code(self):
        self.assertEqual(self.mock_collection.gss_code, "X0100000")

    def test_update_uprn_to_council_model(self):
        self.mock_collection.update_uprn_to_council_model()
        self.assertEqual(UprnToCouncil.objects.get(pk="001").polling_station_id, "1")
        self.assertEqual(UprnToCouncil.objects.get(pk="002").polling_station_id, "")
