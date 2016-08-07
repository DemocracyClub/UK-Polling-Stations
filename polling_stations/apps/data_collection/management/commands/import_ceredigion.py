"""
Import Ceredigion

note: this script takes quite a long time to run
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter

class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Ceredigion
    """
    council_id       = 'W06000008'
    addresses_name   = 'Ceredigion_Addresses_processed.csv'
    stations_name    = 'Ceredigion_Polling_Stations_processed.csv'
    srid             = 27700
    csv_encoding     = 'latin-1'
    elections        = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):

        address = "\n".join([
            record.address1,
            record.address2,
            record.address3,
            record.address4
        ])

        location = Point(float(record.x_coordinate), float(record.y_coordinate), srid=self.get_srid())

        return {
            'internal_council_id': record.polling_station_id,
            'postcode'           : record.postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):

        address = "\n".join([
            record.address1,
            record.street_description,
            record.town_name,
            record.administrative_area
        ])

        return {
            'address'           : address,
            'postcode'          : record.postcode_locator,
            'polling_station_id': record.polling_station_id
        }
