from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_collection.addresshelpers import (
    format_residential_address,
    format_polling_station_address,
)


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id = "E07000241"
    addresses_name = "local.2019-05-02/Version 1/addresses.csv"
    stations_name = "local.2019-05-02/Version 1/stations.csv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","

    def get_station_hash(self, record):
        return "-".join([record.code.strip()])

    def get_station_address(self, record):
        return format_polling_station_address(
            [
                record.address_line1.strip(),
                record.address_line2.strip(),
                record.address_line3.strip(),
                record.address_line4.strip(),
                record.address_line5.strip(),
            ]
        )

    def get_station_point(self, record):
        return None

    def station_record_to_dict(self, record):
        if record.code == "BFB":
            record = record._replace(address_line1="Panshanger Hall")
            record = record._replace(address_line2="Hardings")
            record = record._replace(postcode="AL7 2BQ")
        if record.code in ["BGA", "BGB"]:
            record = record._replace(address_line1="Panshanger Football Club")
        location = self.get_station_point(record)
        code = record.code.strip()
        postcode = record.postcode.strip()

        return {
            "internal_council_id": code,
            "postcode": postcode,
            "address": self.get_station_address(record),
            "location": location,
        }

    def address_record_to_dict(self, record):
        postcode = record.pcode.strip()

        if postcode == "AL69DJ":
            return None

        address = format_residential_address(
            [
                record.electoradd1.strip(),
                record.electoradd2.strip(),
                record.electoradd3.strip(),
                record.electoradd4.strip(),
                record.electoradd5.strip(),
                record.electoradd6.strip(),
            ]
        )

        rec = {
            "address": address.strip(),
            "postcode": record.pcode.strip(),
            "polling_station_id": record.code.strip(),
            "uprn": "",
        }
        return rec
