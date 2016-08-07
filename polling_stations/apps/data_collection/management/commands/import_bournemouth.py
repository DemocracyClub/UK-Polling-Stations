"""
Import Bournemouth Council
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsJsonDistrictsImporter

class Command(BaseCsvStationsJsonDistrictsImporter):
    """
    Imports the Polling station/district data from Bournemouth Council
    """
    council_id     = 'E06000028'
    districts_name = 'Bournemouth_Polling_Districts.geojson'
    stations_name  = 'Polling Stations.csv'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        properties = record['properties']
        if properties['Polling_Districts'] is None:
            return None
        return dict(
            council=self.council,
            internal_council_id=properties['Polling_Districts'],
            name="%s - %s" % (properties['Ward'], properties['Polling_Districts']),
            polling_station_id=properties['Polling_Districts']
        )

    def station_record_to_dict(self, record):
        location = Point(float(record.easting), float(record.northing), srid=self.srid)
        return dict(
            council=self.council,
            internal_council_id=record.polling_station_code,
            postcode=None,
            address=record.location,
            location=location,
            polling_district_id=record.polling_station_code
        )
