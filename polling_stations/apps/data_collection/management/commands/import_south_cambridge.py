"""
Import South Cambridge
"""

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from South Cambridge
    """
    srid           = 27700
    districts_srid = 4326
    council_id     = 'E07000012'
    # districts have not changed since 2015
    districts_name = 'rev01-2015/Polling Districts for Twitter_region'
    # new polling station data provided for 2016
    stations_name  = 'rev02-2016/Polling Stations May 2016_point.shp'
    elections      = [
        'pcc.2016-05-05',
        'ref.2016-06-23'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'name': record[0],
            'polling_station_id': record[1]
        }

    def station_record_to_dict(self, record):

        # format address
        address_parts = record[1].split(" ")
        if address_parts[-1] != 'Chishill' and address_parts[-1] != 'Hinto' and address_parts[-1] != 'CB8':
            postcode = "%s %s" % (address_parts[-2], address_parts[-1])
            del(address_parts[-1])
            del(address_parts[-1])
        else:
            postcode = ''

        address = " ".join(address_parts)
        address = "\n".join(address.split(", "))

        return {
            'internal_council_id': record[-1],
            'postcode'           : postcode,
            'address'            : address
        }
