"""
Import Lambeth Council
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseJasonImporter

class Command(BaseJasonImporter):
    """
    Imports the Polling station/district data from Lambeth Council
    """
    council_id     = 'E06000028'
    districts_name = 'Bournemouth_Polling_Districts.geojson'
    stations_name  = 'Polling Stations.csv'

    def district_record_to_dict(self, record):
        properties = record['properties']
        if properties['Polling_Districts'] is None:
            return
        return dict(
            council=self.council,
            internal_council_id=properties['Polling_Districts'],
            name=properties['Ward'],
        )

    def station_record_to_dict(self, record):
        print record
        location = Point(float(record.easting), float(record.northing), srid=self.srid)
        return dict(
            council=self.council,
            internal_council_id=record.polling_station_code,
            postcode=None,
            address=record.location,
            location=location
        )
