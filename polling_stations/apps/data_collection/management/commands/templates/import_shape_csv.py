"""
Import COUNCIL
"""
import sys

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from COUNCIL
    """
    council_id     = 'COUNCIL_ID'
    districts_name = 'name_without_.shp'
    stations_name  = 'STATION_FILE.csv'
    """
    List of Election IDs the data imported by this script relates to
    https://democracyclub.org.uk/projects/election-ids/
    """
    elections      = []

    def district_record_to_dict(self, record):
        print('District: ', record)
        sys.exit(1)

        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        print('Station: ', record)
        sys.exit(1)

        try:
            location = Point(int(record.easting), int(record.northing), srid=self.get_srid())
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.get_srid())
        return {
            'internal_council_id': record.internal_id,
            'postcode'           : record.address.split(',')[-1],
            'address'            : "\n".join(record.address.split(',')[:-1]),
            'location'           : location
        }
