from django.contrib.gis.geos import Point
from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id      = 'E07000163'
    addresses_name  = 'Craven Property List with UPRNs.csv'
    stations_name   = 'CravePolling Station List.csv'
    elections       = ['local.north-yorkshire.2017-05-04']
    csv_encoding    = 'windows-1253'

    def get_station_point(self, record):
        return Point(
            float(record.easting),
            float(record.northing),
            srid=27700
        )

    def station_record_to_dict(self, record):
        location = self.get_station_point(record)
        return {
            'internal_council_id': record.polling_station_id.strip(),
            'postcode'           : '',
            'address'            : record.name.strip() + "\n" + record.address.strip(),
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.polling_station_id.strip() == '':
            return None

        address = ", ".join([
            record.propertyaddress1,
            record.propertyaddress2,
            record.propertyaddress3,
            record.propertyaddress4,
            record.propertyaddress5,
        ])
        while ", , " in address:
            address = address.replace(", , ", ", ")
        if address[-2:] == ', ':
            address = address[:-2]

        return {
            'address'           : address.strip(),
            'postcode'          : record.propertypostcode.strip(),
            'polling_station_id': record.polling_station_id.strip()
        }
