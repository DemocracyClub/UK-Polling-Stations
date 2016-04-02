"""
Import Brent
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter, import_polling_station_shapefiles


class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Brent Council
    """
    council_id     = 'E09000005'
    districts_name = 'polling_districts'
    stations_name  = 'polling_places.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[-1],
            'name': "%s - %s" % (record[1], record[-1]),
            'polling_station_id': record[-1]
        }

    def station_record_to_dict(self, record):

        # There are 2 records with no address info or code
        # Neither map to a polling station: don't insert them
        if record[2] == 'x':
            return None
        if (isinstance(record[2], bytes)) and\
            (record[2].decode('ascii').strip() == ''):
            return None

        # format/clean up address (a bit)
        if isinstance(record[3], bytes):
            address = record[3].decode('windows-1252')
        else:
            address = record[3]
        address_parts = address.split(', ')
        postcode = ''
        if address_parts[-1][:2] == 'NW' or address_parts[-1][:2] == 'HA':
            postcode = address_parts[-1]
            del(address_parts[-1])
        address = "\n".join(address_parts)

        return {
            'internal_council_id': record[2],
            'postcode'           : postcode,
            'address'            : address
        }

    def import_polling_stations(self):
        import_polling_station_shapefiles(self)
