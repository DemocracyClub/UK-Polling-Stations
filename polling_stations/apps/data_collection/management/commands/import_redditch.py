from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError

class Command(BaseCsvStationsCsvAddressesImporter):
    council_id      = 'E07000236'
    addresses_name  = 'RBC Polling Station look up data.csv'
    stations_name   = 'RBC Polling Station look up data.csv'
    elections       = ['local.worcestershire.2017-05-04']

    def get_station_hash(self, record):
        return "-".join([
            record.pollingplaceid,
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

        # no points supplied, so attempt to attach them by geocoding
        try:
            location_data = geocode_point_only(record.pollingplaceaddress7)
            location = Point(
                location_data['wgs84_lon'],
                location_data['wgs84_lat'],
                srid=4326)
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
        else:
            address = '%s %s' % (record.propertynumber.strip(), record.streetname.strip())

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.pollingplaceid
        }
