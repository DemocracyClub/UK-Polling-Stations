from uk_geo_utils.helpers import Postcode
from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_collection.addresshelpers import (
    format_residential_address,
    format_polling_station_address,
)


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id = "E07000080"
    addresses_name = "parl.2019-12-12/Version 2/POLLINGSTATIONS.csv"
    stations_name = "parl.2019-12-12/Version 2/POLLINGSTATIONS.csv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","

    def get_station_hash(self, record):
        return "-".join([record.polling_district.strip()])

    def get_station_address(self, record):
        return format_polling_station_address(
            [record.polling_station.strip(), record.polling_station_address.strip(),]
        )

    def get_station_point(self, record):
        return None

    def station_record_to_dict(self, record):
        district = record.polling_district.strip()
        location = self.get_station_point(record)

        return {
            "internal_council_id": district,
            "postcode": record.polling_station_postcode.strip(),
            "address": self.get_station_address(record),
            "location": location,
        }

    def address_record_to_dict(self, record):
        address = format_residential_address(
            [
                record.add1.strip(),
                record.add2.strip(),
                record.add3.strip(),
                record.add4.strip(),
                record.add5.strip(),
                record.add6.strip(),
                record.add7.strip(),
                record.add8.strip(),
                record.add9.strip(),
            ]
        ).strip()
        postcode = Postcode(record.postcode.strip(),).without_space
        uprn = record.uprn.lstrip("0").strip()

        if uprn == "10012752190":
            postcode = "GL2 8AA"

        rec = {
            "address": address,
            "postcode": postcode,
            "polling_station_id": record.polling_district.strip(),
            "uprn": uprn,
        }

        return rec
