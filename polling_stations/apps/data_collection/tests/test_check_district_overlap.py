from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from councils.models import Council
from data_collection.base_importers import BaseDistrictsImporter


class StubDistrictsImporter(BaseDistrictsImporter):
    districts_name = "foo"
    districts_filetype = "foo"

    def district_record_to_dict(self, record):
        pass

    def import_data(self):
        pass


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class ImporterTest(TestCase):
    def setUp(self):
        self.stub = StubDistrictsImporter()
        test_council = Council(pk="X01000000")
        test_council.area = GEOSGeometry(
            "MULTIPOLYGON(((-1.8821953907294073 52.702871360302076,-0.37706843760440734 52.702871360302076,-0.37706843760440734 51.9237934761779,-1.8821953907294073 51.9237934761779,-1.8821953907294073 52.702871360302076)))",
            srid=4326,
        )
        self.stub.council = test_council
        self.stub.logger = MockLogger()

    def test_fully_contained(self):
        poly = GEOSGeometry(
            "MULTIPOLYGON(((-1.5635918751044073 52.40227050842306,-0.8824395313544073 52.40227050842306,-0.8824395313544073 52.15356525902296,-1.5635918751044073 52.15356525902296,-1.5635918751044073 52.40227050842306)))",
            srid=4326,
        )
        record = {"area": poly, "internal_council_id": "AA"}
        self.assertEqual(100, self.stub.check_district_overlap(record))

    def test_part_contained(self):
        poly = GEOSGeometry(
            "MULTIPOLYGON(((-1.1406182422919073 52.83747052658817,0.21619328114559266 52.83747052658817,0.21619328114559266 52.346936839550835,-1.1406182422919073 52.346936839550835,-1.1406182422919073 52.83747052658817)))",
            srid=4326,
        )
        record = {"area": poly, "internal_council_id": "AA"}
        percentage = self.stub.check_district_overlap(record)
        self.assertTrue(percentage < 100)
        self.assertTrue(percentage > 0)

    def test_not_contained(self):
        poly = GEOSGeometry(
            "MULTIPOLYGON(((-4.886012959875757 56.89237072129304,-3.7983664755007567 56.89237072129304,-3.7983664755007567 56.53057977266095,-4.886012959875757 56.53057977266095,-4.886012959875757 56.89237072129304)))",
            srid=4326,
        )
        record = {"area": poly, "internal_council_id": "AA"}
        self.assertEqual(0, self.stub.check_district_overlap(record))
