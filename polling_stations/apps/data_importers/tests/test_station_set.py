from addressbase.models import Address, UprnToCouncil
from councils.models import Council
from data_importers.data_types import StationSet
from django.contrib.gis.geos import Point
from django.test import TestCase
from pollingstations.models import PollingStation


def get_addressbase():
    return [
        {
            "uprn": "1",
            "location": Point(0.25, 1),
        },
        {
            "uprn": "2",
            "location": Point(0.75, 1),
        },
        {
            "uprn": "3",
            "location": Point(1, 2),
        },
        {
            "uprn": "4",
            "location": Point(1.75, 3),
        },
    ]


def get_stations():
    return [
        {
            "internal_council_id": "PS-1",
            "council": Council.objects.get(pk="AAA"),
            "polling_district_id": "A",
        },
        {
            "internal_council_id": "PS-2",
            "council": Council.objects.get(pk="AAA"),
            "polling_district_id": "B",
        },
    ]


class StationSetTest(TestCase):
    def setUp(self):
        Council.objects.update_or_create(pk="AAA")

        uprns = ["1", "2", "3", "4"]
        addressbase = get_addressbase()
        polling_stations = get_stations()

        for address in addressbase:
            Address.objects.update_or_create(**address)

        for uprn in uprns:
            UprnToCouncil.objects.update_or_create(pk=uprn, lad="AAA")

        self.station_set = StationSet()
        for element in polling_stations:
            self.station_set.add(element)

    def test_council_id(self):
        self.assertEqual(self.station_set.council_id, "AAA")

    def test_save(self):
        self.station_set.save()
        self.assertEqual(
            set(
                PollingStation.objects.all().values_list(
                    "internal_council_id", "council", "polling_district_id"
                )
            ),
            {("PS-2", "AAA", "B"), ("PS-1", "AAA", "A")},
        )
