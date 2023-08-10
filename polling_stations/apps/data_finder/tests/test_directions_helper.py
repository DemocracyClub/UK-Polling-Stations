import mock
from data_finder.helpers import DirectionsHelper
from data_finder.helpers.directions import Directions, DirectionsException
from django.contrib.gis.geos import Point
from django.test import TestCase

"""
mock get_route() functions for monkey-patching
In these tests we don't care about the outputs
We only care about the source of the result
"""


def mock_route_exception(self, start, end):
    raise DirectionsException("oh noes!! terrible things happened :(")


def mock_route_google(self, start, end):
    return Directions(352, 300, "walk", "foo", 5, "Google", start, end)


def mock_route_mapbox(self, start, end):
    return Directions(352, 300, "walk", "foo", 6, "Mapbox", start, end)


class DirectionsTest(TestCase):
    def setUp(self):
        self.a = Point(-0.14158760012261312, 51.50100893647978, srid=4326)
        self.b = Point(-0.14168760012297544, 51.60100773643453, srid=4326)
        # because we want to get from A to B :)

    def test_bad_params(self):
        # params passed are invalid
        d = DirectionsHelper()
        result = d.get_directions(start_location=False, end_location=False)
        self.assertIsNone(result)

    @mock.patch(
        "data_finder.helpers.directions.MapboxDirectionsClient.get_route",
        mock_route_exception,
    )
    @mock.patch(
        "data_finder.helpers.directions.GoogleDirectionsClient.get_route",
        mock_route_exception,
    )
    def test_all_bad(self):
        # all directions providers throw a DirectionsException
        # get_directions() should return None
        d = DirectionsHelper()
        result = d.get_directions(start_location=self.a, end_location=self.b)
        self.assertIsNone(result)

    @mock.patch(
        "data_finder.helpers.directions.MapboxDirectionsClient.get_route",
        mock_route_exception,
    )
    @mock.patch(
        "data_finder.helpers.directions.GoogleDirectionsClient.get_route",
        mock_route_google,
    )
    def test_google(self):
        # Mapbox throws an exception
        # Fall back to google
        d = DirectionsHelper()
        result = d.get_directions(start_location=self.a, end_location=self.b)
        self.assertEqual("Google", result.source)

    @mock.patch(
        "data_finder.helpers.directions.MapboxDirectionsClient.get_route",
        mock_route_mapbox,
    )
    @mock.patch(
        "data_finder.helpers.directions.GoogleDirectionsClient.get_route",
        mock_route_google,
    )
    def test_mapbox(self):
        # Mapbox returns a valid result
        d = DirectionsHelper()
        result = d.get_directions(start_location=self.a, end_location=self.b)
        self.assertEqual("Mapbox", result.source)

    def test_unit_conversions(self):
        directions = Directions(352, 300, "walk", "", 5, "Test", self.a, self.b)
        self.assertEqual(6, directions.time_in_minutes)
        self.assertEqual("0.2", "{:.1f}".format(directions.distance_in_miles))

    def test_directions_urls(self):
        directions = Directions(352, 300, "walk", "", 5, "Test", self.a, self.b)
        self.assertEqual(
            "https://www.google.com/maps/dir/51.5010,-0.1416/51.6010,-0.1417",
            directions.google_maps_url,
        )
        self.assertEqual(
            "https://www.cyclestreets.net/journey/51.5010,-0.1416/51.6010,-0.1417/",
            directions.cyclestreets_url,
        )
