import json
from os.path import abspath, dirname
from django.test import TestCase
from data_finder.helpers import MapitWrapper


class MapitWrapperMock(MapitWrapper):

    # Mock out the HTTP response from mapit so it returns a known value
    def call_mapit(self):
        return json.load(open(abspath(
            dirname(__file__) + '/../fixtures/mapit_responses/SW1A1AA.json'
        )))


class MapitWrapperTest(TestCase):

    def test_mapit_wrapper(self):
        mapit = MapitWrapperMock('SW1A 1AA')
        result = mapit.geocode()
        self.assertEqual('mapit', result['source'])
        self.assertEqual(-0.14158760012261312, result['wgs84_lon'])
        self.assertEqual(51.50100893647978, result['wgs84_lat'])
        self.assertEqual('E09000033', result['council_gss'])
        self.assertCountEqual(
            ['E14000639', 'E15000007', 'E09000033', 'E32000014', 'E05000644'],
            result['gss_codes']
        )
