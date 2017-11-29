"""
Import Hillingdon
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Hillingdon Council
    """
    council_id = 'E09000017'
    addresses_name = 'Hillingdon PropertyPostCodePollingStationWebLookup-2016-06-08 2.TSV'
    stations_name = 'Hillingdon PropertyPostCodePollingStationWebLookup-2016-06-08 2.TSV'
    csv_delimiter = '\t'
    elections = ['ref.2016-06-23']

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
            record.pollingplaceaddress7,
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
                location = location_data.centroid
            except PostcodeError:
                pass

        return {
            'internal_council_id': record.pollingplaceid,
            'polling_district_id': record.pollingdistrictreference,
            'postcode'           : record.pollingplaceaddress7,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.propertynumber.strip() == '0':
            address = record.streetname.strip()
        else:
            address = '%s %s' % (
                record.propertynumber.strip(), record.streetname.strip())

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.pollingplaceid
        }
