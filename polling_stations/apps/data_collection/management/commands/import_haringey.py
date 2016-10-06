"""
Import Haringey

note: this script takes quite a long time to run
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError

class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Haringey Council
    """
    council_id      = 'E09000014'
    addresses_name  = 'PropertyPostCodePollingStationWebLookup-2016-04-05.TSV'
    stations_name   = 'PollingStations-2016-04-05.tsv'
    csv_delimiter   = '\t'
    elections       = [
        'gla.c.2016-05-05',
        'gla.a.2016-05-05',
        'mayor.london.2016-05-05',
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
        if len(record.pollingplaceaddress7) <= 5:
            location = None
        else:
            try:
                gridref = geocode_point_only(record.pollingplaceaddress7)
                location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None

        return {
            'internal_council_id': record.pollingdistrictreference,
            'postcode'           : record.pollingplaceaddress7,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.propertynumber.strip() == '0':
            address = record.streetname.strip()
        else:
            address = '%s %s' % (record.propertynumber.strip(), record.streetname.strip())

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.pollingdistrictreference
        }
