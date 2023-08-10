import json

from data_finder.helpers.directions import DirectionsException, MapboxDirectionsClient
from django.contrib.gis.geos import Point
from django.test import TestCase


class MapboxDirectionsClientInvalidMock(MapboxDirectionsClient):
    def get_data(self, url):
        return {"code": "oh noes!! terrible things happened :("}


class MapboxDirectionsClientValidMock(MapboxDirectionsClient):
    def get_data(self, url):
        return {
            "routes": [
                {
                    "weight_typical": 3395.485,
                    "duration_typical": 2722.347,
                    "weight_name": "auto",
                    "weight": 3402.205,
                    "duration": 2727.832,
                    "distance": 13276.476,
                    "legs": [
                        {
                            "admins": [
                                {"iso_3166_1_alpha3": "GBR", "iso_3166_1": "GB"}
                            ],
                            "weight_typical": 3395.485,
                            "duration_typical": 2722.347,
                            "weight": 3402.205,
                            "duration": 2727.832,
                            "steps": [],
                            "distance": 13276.476,
                            "summary": "A4, B550",
                        }
                    ],
                    "geometry": "foo\bar",
                }
            ],
            "waypoints": [
                {
                    "distance": 54.085,
                    "name": "Ambassador's Court",
                    "location": [-0.141709, 51.500529],
                },
                {
                    "distance": 80.443,
                    "name": "Grosvenor Road",
                    "location": [-0.141758, 51.600286],
                },
            ],
            "code": "Ok",
            "uuid": "CEQ_Eq3UR9Mo01ygCRYO4TM30JBYPhMh5ToVOM3X1DP8D-DcIgpoAw==",
        }


class GoogleDirectionsClientTest(TestCase):
    def setUp(self):
        self.a = Point(-0.14158760012261312, 51.50100893647978, srid=4326)
        self.b = Point(-0.14168760012297544, 51.60100773643453, srid=4326)
        # because we want to get from A to B :)

    def test_invalid(self):
        m = MapboxDirectionsClientInvalidMock()
        with self.assertRaises(DirectionsException):
            m.get_route(self.a, self.b)

    def test_valid(self):
        m = MapboxDirectionsClientValidMock()
        result = m.get_route(self.a, self.b)
        self.assertEqual(2727.832, result.time)
        self.assertEqual(13276.476, result.distance)
        self.assertEqual(json.dumps("foo\bar"), result.route)
        self.assertEqual(5, result.precision)
        self.assertEqual("Mapbox", result.source)
