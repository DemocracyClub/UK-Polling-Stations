# High-level functional tests for import scripts
from django.db import IntegrityError
from django.test import TestCase

from councils.models import Council
from data_importers.tests.stubs import (
    stub_specialcases,
    stub_duplicatestation,
    stub_duplicatedistrict,
)
from pollingstations.models import PollingDistrict, PollingStation


class ImporterTest(TestCase):

    opts = {"noclean": False, "nochecks": True, "verbosity": 0}

    # create a dummy council which we're going to import data for
    def create_dummy_council(self):
        Council.objects.update_or_create(pk="AAA", identifiers=["X01000000"])

    def test_special_cases(self):
        """
        station_record_to_dict() may optionally return None or a list of dicts.
        district_record_to_dict() may optionally return None.
        Check our base import classes behave as intended in these cases.
        """
        self.create_dummy_council()
        cmd = stub_specialcases.Command()
        cmd.handle(**self.opts)

        districts = PollingDistrict.objects.filter(council_id="AAA").order_by(
            "internal_council_id"
        )
        self.assertEqual(2, len(districts))
        self.assertEqual("AA", districts[0].internal_council_id)
        self.assertEqual("AB", districts[1].internal_council_id)

        stations = PollingStation.objects.filter(council_id="AAA").order_by(
            "internal_council_id"
        )
        self.assertEqual(2, len(stations))
        self.assertEqual("AA", stations[0].internal_council_id)
        self.assertEqual("1 Foo Street", stations[0].address)
        self.assertEqual("AB", stations[1].internal_council_id)
        self.assertEqual("1 Foo Street", stations[1].address)

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
