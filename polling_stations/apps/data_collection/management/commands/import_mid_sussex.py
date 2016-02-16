"""
Imports Mid Sussex
"""
import sys

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseKamlImporter

class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from Mid Sussex
    """
    council_id     = 'E07000228'
    districts_name = 'msdc_3830_pollingdistricts_polygon.kmz'
    stations_name  = 'R3900_pollingstations.csv'

    def station_record_to_dict(self, record):
        location = Point(float(record.xcoord), float(record.ycoord), srid=self.srid)
        address = "\n".join([record.venue, record.street, record.town])
        return {
            'internal_council_id': record.statnum,
            'postcode':            record.postcode,
            'address':             address,
            'location':            location
        }
