import os

from django.test import TestCase

from councils.models import Council
from data_collection.tests import (
    stub_jsonimport,
    stub_jsonimport_different_srids,
    stub_kmlimport,
    stub_kmlimport_different_srids
)
from pollingstations.models import PollingDistrict, PollingStation


# High-level functional tests for import scripts
class ImporterTest(TestCase):

    # create a dummy council which we're going to import data for
    def create_dummy_council(self):
        Council.objects.update_or_create(
            pk='X01000000',
            mapit_id=1,
            council_type='DIS'
        )

    # all of these tests should import the same data
    # from various different source formats
    # so we will run the same checks on the imported data every time
    def run_assertions(self):
        # check we have imported 2 districts
        districts = PollingDistrict.objects.filter(council_id='X01000000')
        self.assertEqual(2, len(districts))

        # check we have imported 3 stations
        stations = PollingStation.objects.filter(council_id='X01000000')
        self.assertEqual(3, len(stations))

        for district in districts:
            polling_stations = PollingStation.objects.filter(location__within=district.area)

            # there should be 1 station in each area
            self.assertEqual(1, len(polling_stations))

            # this point shouldn't be in either district
            self.assertNotEqual('1 Baz Street', polling_stations[0].address)

            # check stations are in the right districts and attributes imported correctly
            if district.name == 'foo':
                self.assertEqual('1 Foo Street', polling_stations[0].address)
                self.assertEqual('XX1 1XX', polling_stations[0].postcode)
            if district.name == 'bar':
                self.assertEqual('1 Bar Street', polling_stations[0].address)
                self.assertEqual('YY1 1YY', polling_stations[0].postcode)

    def test_json_import_srid_4326_csv_4326(self):
        self.create_dummy_council()

        # run our stub importer
        cmd = stub_jsonimport.Command()
        opts = {}
        cmd.handle(**opts)

        self.run_assertions()

    def test_json_import_srid_4326_csv_27700(self):
        self.create_dummy_council()

        # run our stub importer
        cmd = stub_jsonimport_different_srids.Command()
        opts = {}
        cmd.handle(**opts)

        self.run_assertions()

    def test_kml_import_srid_4326_csv_4326(self):
        self.create_dummy_council()

        # run our stub importer
        cmd = stub_kmlimport.Command()
        opts = {}
        cmd.handle(**opts)

        self.run_assertions()

    def test_kml_import_srid_4326_csv_27700(self):
        self.create_dummy_council()

        # run our stub importer
        cmd = stub_kmlimport_different_srids.Command()
        opts = {}
        cmd.handle(**opts)

        self.run_assertions()
