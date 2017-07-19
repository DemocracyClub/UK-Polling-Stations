import json
from django.contrib.gis.geos import Point
from django.test import TestCase
from data_finder.directions_clients import (
    DirectionsException, MapzenDirectionsClient)


class MapzenDirectionsClientInvalidMock(MapzenDirectionsClient):

    def get_data(self, url):
        return {
            'trip': {
                'status': 'oh noes!! terrible things happened :('
            }
        }


class MapzenDirectionsClientNoApiKeyMock(MapzenDirectionsClient):

    def get_api_key(self):
        return ''


class MapzenDirectionsClientValidMock(MapzenDirectionsClient):

    def get_api_key(self):
        return 'foobarbaz'

    def get_data(self, url):
        return {
            'trip': {
                'status': 0,
                'summary': {
                    'time': 600,
                    'length': 0.457,
                },
                'legs': [
                    {
                        'shape': 'foo\bar'
                    }
                ]
            },
        }

class MapzenDirectionsClientTest(TestCase):

    def setUp(self):
        self.a = Point(-0.14158760012261312, 51.50100893647978, srid=4326)
        self.b = Point(-0.14168760012297544, 51.60100773643453, srid=4326)
        # because we want to get from A to B :)

    def test_invalid(self):
        m = MapzenDirectionsClientInvalidMock()
        with self.assertRaises(DirectionsException):
            m.get_route(self.a, self.b)

    def test_no_api_key(self):
        m = MapzenDirectionsClientNoApiKeyMock()
        with self.assertRaises(DirectionsException):
            m.get_route(self.a, self.b)

    def test_valid(self):
        m = MapzenDirectionsClientValidMock()
        result = m.get_route(self.a, self.b)
        self.assertEqual('10 minute', result.time)
        self.assertEqual('0.5 miles', result.dist)
        self.assertEqual(json.dumps('foo\bar'), result.route)
        self.assertEqual(6, result.precision)
        self.assertEqual('Mapzen', result.source)
