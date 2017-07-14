import mock
from django.contrib.gis.geos import Point
from django.test import TestCase
from data_finder.directions_clients import (
    Directions,
    DirectionsException,
    GoogleDirectionsClient,
    MapzenDirectionsClient
)
from data_finder.helpers import DirectionsHelper


"""
mock get_route() functions for monkey-patching
In these tests we don't care about the outputs
We only care about the source of the result
"""
def mock_route_exception(self, start, end):
    raise DirectionsException('oh noes!! terrible things happened :(')

def mock_route_google(self, start, end):
    return Directions(
        '1', '1', 'foo', 5, 'Google')

def mock_route_mapzen(self, start, end):
    return Directions(
        '1', '1', 'foo', 6, 'Mapzen')


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

    @mock.patch("data_finder.directions_clients.MapzenDirectionsClient.get_route", mock_route_exception)
    @mock.patch("data_finder.directions_clients.GoogleDirectionsClient.get_route", mock_route_exception)
    def test_all_bad(self):
        # all directions providers throw a DirectionsException
        # get_directions() should return None
        d = DirectionsHelper()
        result = d.get_directions(start_location=self.a, end_location=self.b)
        self.assertIsNone(result)

    @mock.patch("data_finder.directions_clients.MapzenDirectionsClient.get_route", mock_route_exception)
    @mock.patch("data_finder.directions_clients.GoogleDirectionsClient.get_route", mock_route_google)
    def test_google(self):
        # Mapzen throws an exception
        # Fall back to google
        d = DirectionsHelper()
        result = d.get_directions(start_location=self.a, end_location=self.b)
        self.assertEqual('Google', result.source)

    @mock.patch("data_finder.directions_clients.MapzenDirectionsClient.get_route", mock_route_mapzen)
    @mock.patch("data_finder.directions_clients.GoogleDirectionsClient.get_route", mock_route_google)
    def test_mapzen(self):
        # Mapzen returns a valid result
        d = DirectionsHelper()
        result = d.get_directions(start_location=self.a, end_location=self.b)
        self.assertEqual('Mapzen', result.source)
