from django.contrib.gis.geos import Point
from django.test import TestCase
from pollingstations.models import PollingStation


# define the conditions we are going to test for here
# we will run these tests against fixtures
# which create the same set of conditions in different ways
class PollingStationsTestBase:
    def test_good(self):
        # this point will be in district AA
        point = Point(-2.1588134765625, 52.8193630015979)
        station = PollingStation.objects.get_polling_station(
            "X01000001", location=point
        )
        # this district maps to one polling station in area X01000001
        self.assertEqual("1", station.internal_council_id)
        self.assertEqual("St Foo's Church Hall, Bar Town", station.address)

    def test_multiple_matches(self):
        # this point will be in district BB
        point = Point(0.76904296875, 53.1434755845945)
        station = PollingStation.objects.get_polling_station(
            "X01000001", location=point
        )
        # this district maps to two polling stations
        # in area X01000001 so we expect station=None
        self.assertIsNone(station)

    def test_no_matches(self):
        # this point will be in district CC
        point = Point(-4.3341064453125, 55.85835810656004)
        station = PollingStation.objects.get_polling_station(
            "X01000001", location=point
        )
        # this district maps to no polling stations
        # in area X01000001 so we expect station=None
        self.assertIsNone(station)


# test lookup when PollingDistrict.station_id is set
class PollingStationsStationIdTest(TestCase, PollingStationsTestBase):
    fixtures = ["test_polling_stations_station_id.json"]

    def test_multiple_matches(self):
        pass


# test lookup when PollingStation.district_id is set
class PollingStationsDistrictIdTest(TestCase, PollingStationsTestBase):
    fixtures = ["test_polling_stations_district_id.json"]


# test lookup when we match based on point in polygon
class PollingStationsPointInPolygonTest(TestCase, PollingStationsTestBase):
    fixtures = ["test_polling_stations_polygon.json"]

    def test_good(self):
        # this point will be in district AA
        point = Point(-2.1588134765625, 52.8193630015979)
        station = PollingStation.objects.get_polling_station(
            "X01000001", location=point
        )
        # district AA has a blank station refernce
        self.assertIsNone(station)
