"""
Import Neath Port Talbot

note: this script takes quite a long time to run
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseCsvStationsCsvAddressesImporter,
    import_polling_station_shapefiles
)

class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Neath Port Talbot
    """
    council_id       = 'W06000012'
    addresses_name   = 'polling_properties.csv'
    stations_name    = 'polling_stations_updated.shp'
    srid             = 27700
    elections        = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]

    # polling stations provided as shape files, not csv
    def import_polling_stations(self):
        import_polling_station_shapefiles(self)

    def station_record_to_dict(self, record):

        # format address
        address_parts = []
        address_parts.append(record[2])
        for i in range(4,8):
            if record[i].strip():
                address_parts.append(record[i].strip())
        address = "\n".join(address_parts)

        return {
            'internal_council_id': record[1],
            'postcode'           : record[8],
            'address'            : address
        }

    def address_record_to_dict(self, record):

        # format address
        if record.substreetn:
            address1 = "%s %s %s" % (record.housename, record.housenumbe, record.substreetn)
            address1 = address1.strip()
            address2 = record.streetname
        else:
            address1 = "%s %s %s" % (record.housename, record.housenumbe, record.streetname)
            address1 = address1.strip()
            address2 = ""

        address = "\n".join([
            address1,
            address2,
            record.locality,
            record.town
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")

        return {
            'address'           : address,
            'postcode'          : record.housepostc,
            'polling_station_id': record.pollingdis
        }
