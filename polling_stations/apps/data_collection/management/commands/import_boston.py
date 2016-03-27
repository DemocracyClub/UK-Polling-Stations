"""
Import Boston
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Boston Council
    """
    council_id = 'E07000136'
    districts_name = 'Polling Districts May 2015_region'
    stations_name = 'pollingstations.csv'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)

        address_parts = [x.strip() for x in record.address.split(',')]
        address = "\n".join(address_parts[:-1])
        postcode = address_parts[-1]

        return {
            'internal_council_id': record.internal_id,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }
