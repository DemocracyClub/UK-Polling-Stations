"""
Import South Tyneside
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter, import_polling_station_shapefiles

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from South Tyneside Council
    """
    council_id     = 'E08000023'
    districts_name = 'Polling Districts_region'
    stations_name  = 'Polling Sites.csv'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        return
        location = Point(float(record.lat), float(record.long), srid=4326)
        raise Exception('The points are wrong - we tried to set them manually ')
        return {
            'internal_council_id': record.polling_district,
            'postcode'           : '(no postcode supplied)',
            'address'            : "\n".join(record.address.split(',')),
            'location'           : location
        }
    
