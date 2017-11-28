from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id      = 'E08000016'
    addresses_name  = 'parl.2017-06-08/Version 1/Democracy Club File-withheaders.csv'
    stations_name   = 'parl.2017-06-08/Version 1/Democracy Club File-withheaders.csv'
    elections       = ['parl.2017-06-08']

    def get_station_hash(self, record):
        return "-".join([
            record.code.strip(),
        ])

    def get_station_address(self, record):
        address = "\n".join([
            record.station_add1.strip(),
            record.station_add2.strip(),
            record.station_add3.strip(),
            record.station_add4.strip(),
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")
        return address.strip()

    def get_station_point(self, record):
        postcode = record.station_postcode.strip()
        if postcode == '':
            return None

        try:
            location_data = geocode_point_only(postcode)
            location = location_data.centroid
        except PostcodeError:
            location = None
        return location

    def station_record_to_dict(self, record):
        location = self.get_station_point(record)
        return {
            'internal_council_id': record.code.strip(),
            'postcode'           : record.station_postcode.strip(),
            'address'            : self.get_station_address(record),
            'location'           : location
        }

    def address_record_to_dict(self, record):
        address = ", ".join([
            record.add1.strip(),
            record.add2.strip(),
        ])
        while ", , " in address:
            address = address.replace(", , ", ", ")
        if address[-2:] == ', ':
            address = address[:-2]

        return {
            'address'           : address.strip(),
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.code.strip(),
        }
