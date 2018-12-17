import json
from django.contrib.gis.geos import Point
from django.test import TestCase
from data_finder.helpers.directions import (
    DirectionsException, GoogleDirectionsClient)


class GoogleDirectionsClientInvalidMock(GoogleDirectionsClient):

    def get_data(self, url):
        return {
            'status': 'oh noes!! terrible things happened :('
        }


class GoogleDirectionsClientValidMock(GoogleDirectionsClient):

    def get_data(self, url):
        return {
            'status': 'OK',
            'routes': [
                {
                    'legs': [
                        {
                            'duration': {
                                'text': '4 mins'
                            },
                            'distance': {
                                'text': '0.2 mi'
                            }
                        }
                    ],
                    'overview_polyline': {
                        'points': 'foo\bar'
                    }
                }
            ]
        }


class GoogleDirectionsClientTest(TestCase):

    def setUp(self):
        self.a = Point(-0.14158760012261312, 51.50100893647978, srid=4326)
        self.b = Point(-0.14168760012297544, 51.60100773643453, srid=4326)
        # because we want to get from A to B :)

    def test_invalid(self):
        g = GoogleDirectionsClientInvalidMock()
        with self.assertRaises(DirectionsException):
            g.get_route(self.a, self.b)

    def test_valid(self):
        g = GoogleDirectionsClientValidMock()
        result = g.get_route(self.a, self.b)
        self.assertEqual('4 minute', result.time)
        self.assertEqual('0.2 miles', result.dist)
        self.assertEqual(json.dumps('foo\bar'), result.route)
        self.assertEqual(5, result.precision)
        self.assertEqual('Google', result.source)
