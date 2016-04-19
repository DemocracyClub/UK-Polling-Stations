"""
Imports Chorley
"""
import sys

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseKamlImporter

class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from Chorley
    """
    council_id     = 'E07000118'
    districts_name = 'Chorley Polling Districts.kmz'
    stations_name  = 'Chorley_Polling_Stations.csv'
    elections      = ['parl.2015-05-07']

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.point_x), int(record.point_y), srid=self.srid)
        except ValueError:
            location = Point(float(record.point_x), float(record.point_y), srid=self.srid)
        return {
            'internal_council_id': record.objectid,
            'postcode': self.postcode_from_address(record.address),
            'address':  "\n".join(record.address.split(',')[:-1]),
            'location': location
        }
