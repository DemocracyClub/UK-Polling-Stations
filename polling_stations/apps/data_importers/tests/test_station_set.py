from django.contrib.gis.geos import Polygon, Point, MultiPolygon
from django.test import TestCase

from addressbase.models import Address, UprnToCouncil
from councils.models import Council
from data_importers.data_types import StationSet
from pollingstations.models import PollingDistrict, PollingStation


def get_uprns():
    return [
        {"uprn": "1", "lad": "AAA"},
        {"uprn": "2", "lad": "AAA"},
        {"uprn": "3", "lad": "AAA"},
        {"uprn": "4", "lad": "AAA"},
    ]


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


def get_districts():
    return [
        {
            "area": MultiPolygon(Polygon(((0, 0), (0, 3), (1, 3), (1, 0), (0, 0)))),
            "council": Council.objects.get(pk="AAA"),
            "internal_council_id": "A",
        },
        {
            "area": MultiPolygon(Polygon(((1, 1), (1, 4), (2, 4), (2, 1), (1, 1)))),
            "council": Council.objects.get(pk="AAA"),
            "internal_council_id": "B",
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

        uprns = get_uprns()
        polling_districts = get_districts()
        addressbase = get_addressbase()
        polling_stations = get_stations()
        for district in polling_districts:
            PollingDistrict.objects.update_or_create(**district)

        for address in addressbase:
            Address.objects.update_or_create(**address)

        for uprn in uprns:
            UprnToCouncil.objects.update_or_create(**uprn)

        for station in polling_stations:
            PollingStation.objects.update_or_create(**station)

        self.station_set = StationSet()
        for element in polling_stations:
            self.station_set.add(element)

    def test_council_id(self):
        self.assertEqual(self.station_set.council_id, "AAA")

    def test_get_polling_station_lookup(self):
        expected = {"PS-1": {"1", "2"}, "PS-2": {"4"}}

        self.assertEqual(self.station_set.get_polling_station_lookup(), expected)
