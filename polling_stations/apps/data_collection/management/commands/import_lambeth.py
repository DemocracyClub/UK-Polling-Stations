"""
Import Lambeth Council
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseJasonImporter

class Command(BaseJasonImporter):
    """
    Imports the Polling station/district data from Lambeth Council
    """
    council_id     = 'E09000022'
    districts_name = 'LambethPollingDistricts.json'
    stations_name  = 'LambethPollingStations_0.csv'

    def district_record_to_dict(self, record):
        properties = record['properties']
        return dict(
            council=self.council,
            internal_council_id=properties['DISTRICT_C'],
            extra_id=properties['OBJECTID'],
            name="%s - %s" % (properties['WARD'], properties['DISTRICT_C']),
            polling_station_id=properties['DISTRICT_C']
        )

    def station_record_to_dict(self, record):
        location = Point(int(record.easting), int(record.northing), srid=self.srid)
        return dict(
            council=self.council,
            internal_council_id=record.district_code,
            postcode=record.postcode,
            address="\n".join([record.venue, record.address]),
            location=location,
            polling_district_id=record.district_code
        )
