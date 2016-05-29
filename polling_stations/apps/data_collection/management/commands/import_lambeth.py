"""
Import Lambeth

note: this script takes quite a long time to run
"""
from time import sleep
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, PostcodeError

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Lambeth Council
    """
    council_id      = 'E09000022'
    addresses_name  = 'rev02-2016/Lambeth PropertyPostCodePollingStationWebLookup-2016-05-26.TSV'
    stations_name   = 'rev02-2016/PollingStations-2016-05-26.tsv'
    csv_delimiter   = '\t'
    elections       = [
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):

        # format address
        address = "\n".join([
            record.pollingplaceaddress1,
            record.pollingplaceaddress2,
            record.pollingplaceaddress3,
            record.pollingplaceaddress4,
            record.pollingplaceaddress5,
            record.pollingplaceaddress6,
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        # no points supplied, so attempt to attach them by geocoding
        sleep(1.3) # ensure we don't hit mapit's usage limit
        if len(record.pollingplaceaddress7) <= 5:
            location = None
        else:
            try:
                gridref = geocode(record.pollingplaceaddress7)
                location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None

        return {
            'internal_council_id': record.pollingplaceid,
            'postcode'           : record.pollingplaceaddress7,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.propertynumber.strip() == '0':
            address = record.streetname.strip()

            """
            There are 2 cases where the same "address" maps to 2
            different polling stations due to incomplete data.
            We will just exclude them for convenience - its a drop in the ocean.
            """
            if address == 'Rectory Grove' or address == 'Kennington Oval':
                return None

        else:
            address = '%s %s' % (record.propertynumber.strip(), record.streetname.strip())

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.pollingplaceid
        }
