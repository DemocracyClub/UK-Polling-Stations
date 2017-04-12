import json
from os.path import abspath, dirname
from django.test import TestCase
from data_finder.helpers import MapitGeocoder, PostcodeError


class MapitGeocoderValidMock(MapitGeocoder):

    # Mock out the HTTP response from mapit so it returns a known good value
    def call_mapit(self):
        return json.load(open(abspath(
            dirname(__file__) + '/../fixtures/mapit_responses/SW1A1AA.json'
        )))

class MapitGeocoderNoLocationMock(MapitGeocoder):

    # Mock out the HTTP response from mapit so it returns a known bad value
    def call_mapit(self):
        return {"postcode": "JE3 7DW", "areas": {}}


class MapitGeocoderValidTest(TestCase):

    def test_mapit_geocoder(self):
        mapit = MapitGeocoderValidMock('SW1A 1AA')
        result = mapit.geocode()
        self.assertEqual('mapit', result['source'])
        self.assertEqual(-0.14158760012261312, result['wgs84_lon'])
        self.assertEqual(51.50100893647978, result['wgs84_lat'])
        self.assertEqual('E09000033', result['council_gss'])
        self.assertCountEqual(
            ['E14000639', 'E15000007', 'E09000033', 'E32000014', 'E05000644'],
            result['gss_codes']
        )

class MapitGeocoderNoLocationTest(TestCase):

    def test_mapit_geocoder(self):
        mapit = MapitGeocoderNoLocationMock('JE3 7DW')
        self.assertRaises(PostcodeError, mapit.geocode)
