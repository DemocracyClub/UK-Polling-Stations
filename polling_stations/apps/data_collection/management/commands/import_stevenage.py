from django.core.exceptions import ObjectDoesNotExist
from data_collection.addresshelpers import format_polling_station_address
from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError
from uk_geo_utils.geocoders import AddressBaseGeocoder, AddressBaseException


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id      = 'E07000243'
    addresses_name  = 'local.2018-05-03/Version 1/DemocracyClub Stevenage PD removed.csv'  # from idox
    stations_name   = 'local.2018-05-03/Version 1/stations.csv'  # extracted from PDF by hand
    elections       = ['local.2018-05-03']

    def format_address(self, instr):
        address = instr.replace('; ', ", ").strip()
        if address[-1] == ',':
            address = address[:-1]
        postcode = address.split(', ')[-1]
        address = ', '.join(address.split(', ')[:-1])
        return (address, postcode)

    def address_record_to_dict(self, record):
        address, postcode = self.format_address(record.address)

        if postcode == 'SG1 4XS':
            return None

        return {
            'uprn': '',
            'address': address,
            'postcode': postcode,
            'polling_station_id': record.refer[:3],
        }

    def geocode_from_postcode(self, record):
        try:
            location_data = geocode_point_only(record.postcode)
            return location_data.centroid
        except PostcodeError:
            return None

    def get_station_point(self, record):
        if record.uprn and record.uprn != '0':
            uprn = record.uprn.lstrip('0')
            try:
                g = AddressBaseGeocoder(record.postcode)
                return g.get_point(record.uprn)
            except (ObjectDoesNotExist, AddressBaseException) as e:
                return self.geocode_from_postcode(record)
        else:
            return self.geocode_from_postcode(record)

    def station_record_to_dict(self, record):
        address_parts = [
            record.address1,
            record.address2,
            record.address3,
            record.address4,
        ]
        if record.address5:
            address_parts.append(record.address5)
        address = format_polling_station_address(address_parts)
        return {
            'internal_council_id': record.code,
            'postcode': record.postcode,
            'address': address,
            'location': self.get_station_point(record),
        }
