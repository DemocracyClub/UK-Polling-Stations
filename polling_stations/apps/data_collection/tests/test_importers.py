from django.db.utils import IntegrityError
from django.test import TestCase

from councils.models import Council
from data_collection.tests.stubs import (
    stub_addressimport,
    stub_duplicatedistrict,
    stub_duplicatestation,
    stub_jsonimport,
    stub_jsonimport_different_srids,
    stub_kmlimport,
    stub_kmlimport_different_srids,
    stub_specialcases,
)
from pollingstations.models import (
    PollingDistrict, PollingStation, ResidentialAddress)


# High-level functional tests for import scripts
class ImporterTest(TestCase):

    opts = {
        'noclean': False,
        'nochecks': True,
        'verbosity': 0
    }

    # create a dummy council which we're going to import data for
    def create_dummy_council(self):
        Council.objects.update_or_create(pk='X01000000')

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
        cmd.handle(**self.opts)

        self.run_assertions()

    def test_json_import_srid_4326_csv_27700(self):
        self.create_dummy_council()

        # run our stub importer
        cmd = stub_jsonimport_different_srids.Command()
        cmd.handle(**self.opts)

        self.run_assertions()

    def test_kml_import_srid_4326_csv_4326(self):
        self.create_dummy_council()

        # run our stub importer
        cmd = stub_kmlimport.Command()
        cmd.handle(**self.opts)

        self.run_assertions()

    def test_kml_import_srid_4326_csv_27700(self):
        self.create_dummy_council()

        # run our stub importer
        cmd = stub_kmlimport_different_srids.Command()
        cmd.handle(**self.opts)

        self.run_assertions()

    def test_special_cases(self):
        """
        station_record_to_dict() may optionally return None or a list of dicts.
        district_record_to_dict() may optionally return None.
        Check our base import classes behave as intended in these cases.
        """
        self.create_dummy_council()
        cmd = stub_specialcases.Command()
        cmd.handle(**self.opts)

        districts = PollingDistrict.objects\
                                   .filter(council_id='X01000000')\
                                   .order_by('internal_council_id')
        self.assertEqual(2, len(districts))
        self.assertEqual('AA', districts[0].internal_council_id)
        self.assertEqual('AB', districts[1].internal_council_id)

        stations = PollingStation.objects\
                                 .filter(council_id='X01000000')\
                                 .order_by('internal_council_id')
        self.assertEqual(2, len(stations))
        self.assertEqual('AA', stations[0].internal_council_id)
        self.assertEqual('1 Foo Street', stations[0].address)
        self.assertEqual('AB', stations[1].internal_council_id)
        self.assertEqual('1 Foo Street', stations[1].address)

    def test_duplicate_stations(self):
        """
        Check that if we try to insert a duplicate station on
        (council_id, internal_council_id) an IntegrityError is thrown
        """
        self.create_dummy_council()
        cmd = stub_duplicatestation.Command()
        exception_thrown = False
        try:
            cmd.handle(**self.opts)
        except IntegrityError:
            exception_thrown = True

        self.assertTrue(exception_thrown)

    def test_duplicate_districts(self):
        """
        Check that if we try to insert a duplicate district on
        (council_id, internal_council_id) an IntegrityError is thrown
        """
        self.create_dummy_council()
        cmd = stub_duplicatedistrict.Command()
        exception_thrown = False
        try:
            cmd.handle(**self.opts)
        except IntegrityError:
            exception_thrown = True

        self.assertTrue(exception_thrown)

    def test_address_import(self):
        self.create_dummy_council()
        cmd = stub_addressimport.Command()
        cmd.handle(**self.opts)

        addresses = ResidentialAddress.objects\
                                      .filter(council_id='X01000000')\
                                      .order_by('address')\
                                      .values_list('address', flat=True)

        self.assertEqual(3, len(addresses))
        expected = set([
            '36 Abbots Park, London',
            '3 Factory Rd, Poole',
            '80 Pine Vale Cres, Bournemouth',
        ])
        self.assertEqual(set(addresses), expected)
