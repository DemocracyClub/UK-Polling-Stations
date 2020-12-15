from django.test import TestCase

from addressbase.models import UprnToCouncil, Address
from councils.models import Council
from data_importers.data_types import AssignPollingStationsMixin


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
        mock_collection = MockCollection()
        mock_collection.elements = [{}]

    def test_update_uprn_to_council_model(self):
        Council.objects.update_or_create(pk="Foo")
        Address.objects.update_or_create(pk="001")
        Address.objects.update_or_create(pk="002")
        UprnToCouncil.objects.update_or_create(pk="001", lad="Foo")
        UprnToCouncil.objects.update_or_create(pk="002", lad="Foo")
        mock_collection = MockCollection()
        mock_collection.elements = [{"council": Council.objects.get(pk="Foo")}]
        mock_collection.update_uprn_to_council_model()

        self.assertEqual(UprnToCouncil.objects.get(pk="001").polling_station_id, "1")
        self.assertEqual(UprnToCouncil.objects.get(pk="002").polling_station_id, "")
