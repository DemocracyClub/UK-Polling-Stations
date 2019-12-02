from addressbase.models import Address
from uk_geo_utils.helpers import Postcode
from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_collection.addresshelpers import (
    format_residential_address,
    format_polling_station_address,
)


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id = "W06000020"
    addresses_name = "parl.2019-12-12/Version 1/DEMOCRACY CLUB Finaltor.csv"
    stations_name = "parl.2019-12-12/Version 1/DEMOCRACY CLUB Finaltor.csv"
    elections = ["parl.2019-12-12"]

    def get_station_hash(self, record):
        return "-".join([record.polling_district.strip()])

    def get_station_address(self, record):
        return format_polling_station_address(
            [
                record.polling_station_name.strip(),
                record.polling_station_address1.strip(),
                record.polling_station_address2.strip(),
                record.polling_station_address3.strip(),
                record.polling_station_address4.strip(),
                record.polling_station_address5.strip(),
                record.polling_station_address6.strip(),
                record.polling_station_address7.strip(),
                record.polling_station_address8.strip(),
            ]
        )

    def get_station_point(self, record):
        uprn = record.polling_station_uprn.lstrip("0").strip()
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except Address.DoesNotExist:
            return None

    def station_record_to_dict(self, record):
        location = self.get_station_point(record)
        return {
            "internal_council_id": record.polling_district.strip(),
            "postcode": record.polling_station_address9.strip(),
            "address": self.get_station_address(record),
            "location": location,
        }

    def address_record_to_dict(self, record):
        address = format_residential_address(
            [
                record.elector_address1.strip(),
                record.elector_address2.strip(),
                record.elector_address3.strip(),
                record.elector_address4.strip(),
                record.elector_address5.strip(),
                record.elector_address6.strip(),
                record.elector_address7.strip(),
                record.elector_address8.strip(),
            ]
        )

        return {
            "address": address.strip(),
            "postcode": Postcode(record.elector_address9.strip()).without_space,
            "polling_station_id": record.polling_district.strip(),
        }
