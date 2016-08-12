"""
Import Edinburgh (revision 02)
"""
import shapefile, sys
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Edinburgh
    """
    council_id     = 'S12000036'
    districts_name = 'rev02-2016/polling district boundaries 2016'
    """
    Edinburgh have supplied a seperate stations file,
    but it is missing a couple of stations
    (even after accounting for stations serving more than one district)
    However, the districts file also includes
    the polling place names, addresses and points
    (except one that has no address, postcode or co-ordinates)
    We will parse the districts file twice and pull the station data from there
    This will provide coverage for all but one of the districts.
    """
    stations_name  = 'rev02-2016/polling district boundaries 2016.shp'
    elections      = [
        'sp.c.2016-05-05',
        'sp.r.2016-05-05',
        'ref.2016-06-23'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': "%s - %s" % (record[1], record[0]),
            'polling_station_id': record[0]
        }

    def station_record_to_dict(self, record):

        # don't insert the blank station record
        if (isinstance(record[6], bytes)) and\
            (record[6].decode('ascii').strip() == ''):
            return None

        # polling station point is in shape attributes
        location = Point(float(record[9]), float(record[10]), srid=self.get_srid())

        # format address
        if isinstance(record[5], bytes):
            address = "%s, %s" % (record[5].decode('latin-1'), record[6])
        else:
            address = "%s, %s" % (record[5], record[6])

        return {
            'internal_council_id': record[0],
            'postcode': record[7],
            'address': "\n".join(address.split(', ')),
            'location': location
        }
