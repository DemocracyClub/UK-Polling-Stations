"""
Import Dundee
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsJsonDistrictsImporter

class Command(BaseCsvStationsJsonDistrictsImporter):
    """
    Imports the Polling station/district data from Dundee Council
    """
    council_id     = 'S12000042'
    districts_name = 'polling_districts.bng.geo.json'
    stations_name  = 'SV_POLLING_STATIONS.csv'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        properties = record['properties']
        return {
            'council':             self.council,
            'internal_council_id': properties['POLLING_DISTRICT'],
            'name':                properties['POLLING_STATION_NAME']
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.easting), float(record.northing), srid=self.srid)

        """
        address data is sufficiently poor quality that
        geocoding is likely to produce misleading results
        """

        return {
            'council':             self.council,
            'internal_council_id': record.objectid,
            'postcode':            "",
            'address':             record.name,
            'location':            location,
            'polling_district_id': record.polling_district
        }
