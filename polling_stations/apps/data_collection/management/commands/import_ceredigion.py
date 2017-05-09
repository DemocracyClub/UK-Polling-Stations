from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from addressbase.models import Address

class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Ceredigion
    """
    council_id       = 'W06000008'
    addresses_name   = 'Ceredigion_Properties_withheaders.csv'
    stations_name    = 'Ceredigion_Polling_Stations_processed.csv'
    srid             = 27700
    csv_encoding     = 'latin-1'
    elections        = [
        'local.ceredigion.2017-05-04',
        'parl.2017-06-08'
    ]

    def station_record_to_dict(self, record):

        address = "\n".join([
            record.address1,
            record.address2,
            record.address3,
            record.address4
        ])

        location = Point(
            float(record.x_coordinate),
            float(record.y_coordinate),
            srid=self.get_srid()
        )

        return {
            'internal_council_id': record.polling_station_id,
            'postcode'           : record.postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):

        try:
            address = Address.objects.get(pk=record.uprn)
        except ObjectDoesNotExist:
            return None

        return {
            'address': address.address,
            'postcode': address.postcode,
            'polling_station_id': record.station,
        }
