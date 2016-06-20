"""
Import Islington
"""
from time import sleep
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Islington Council
    """
    council_id      = 'E09000019'
    addresses_name  = '2016/PropertyPostCodePollingStationWebLookup-2016-06-13 2.TSV'
    stations_name   = '2016/PropertyPostCodePollingStationWebLookup-2016-06-13 2.TSV'
    csv_delimiter   = '\t'
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):
            return "-".join([
                record.pollingplaceaddress7,
                record.pollingplaceid,
                record.pollingdistrictreference,
            ])


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


        location = None
        location_data = None
        if int(record.pollingplaceeasting) and int(record.pollingplacenorthing):
            location = Point(
                float(record.pollingplaceeasting),
                float(record.pollingplacenorthing),
                srid=27700)
        else:
            # no points supplied, so attempt to attach them by geocoding
            try:
                location_data = geocode_point_only(record.pollingplaceaddress7)
            except PostcodeError:
                pass

            if location_data:
                location = Point(
                    location_data['wgs84_lon'],
                    location_data['wgs84_lat'],
                    srid=4326)

        return {
            'internal_council_id': record.pollingplaceid,
            'postcode'           : record.pollingplaceaddress7,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        postcode = record.postcode.strip()

        if record.propertynumber.strip() == '0':
            address = record.streetname.strip()
        else:
            address = ' '.join([
                record.propertynumber.strip(),
                record.streetname.strip()
            ])

        return {
            'address'           : address,
            'postcode'          : postcode,
            'polling_station_id': record.pollingplaceid
        }
