from uk_geo_utils.helpers import Postcode
from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError
from data_collection.addresshelpers import (
    format_residential_address,
    format_polling_station_address,
)


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id = "E06000057"
    addresses_name = "mayor.2019-05-02/Version 1/MAYORAL DATA.csv"
    stations_name = "mayor.2019-05-02/Version 1/MAYORAL DATA.csv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def get_station_hash(self, record):
        return "-".join([record.col1.strip()])

    def get_station_address(self, record):
        return format_polling_station_address(
            [
                record.col7.strip(),
                record.col8.strip(),
                record.col9.strip(),
                record.col10.strip(),
                record.col11.strip(),
                record.col12.strip(),
            ]
        )

    def get_station_point(self, record):
        postcode = record.col13.strip()
        if postcode == "":
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
            "internal_council_id": record.col1.strip(),
            "postcode": record.col13.strip(),
            "address": self.get_station_address(record),
            "location": location,
        }

    def address_record_to_dict(self, record):
        address = format_residential_address(
            [
                record.col2.strip(),
                record.col3.strip(),
                record.col4.strip(),
                record.col5.strip(),
            ]
        ).strip()
        postcode = Postcode(record.col6.strip()).without_space

        rec = {
            "address": address,
            "postcode": postcode,
            "polling_station_id": record.col1.strip(),
            "uprn": "",
        }

        return rec
