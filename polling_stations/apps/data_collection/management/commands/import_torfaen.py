from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id = "W06000020"
    addresses_name = "parl.2017-06-08/Version 1/ElectorateAddressWthPollingStationsTorfaenFINAL-anonymised.csv"
    stations_name = "parl.2017-06-08/Version 1/ElectorateAddressWthPollingStationsTorfaenFINAL-anonymised.csv"
    elections = ["parl.2017-06-08"]

    def get_station_hash(self, record):
        return "-".join([record.station_uprn.strip()])

    def get_station_address(self, record):
        address = "\n".join(
            [
                record.polling_station_name.strip(),
                record.polling_station_address1.strip(),
                record.polling_station_address2.strip(),
                record.polling_station_address3.strip(),
                record.polling_station_address4.strip(),
                record.polling_station_address5.strip(),
            ]
        )
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")
        return address.strip()

    def get_station_point(self, record):
        postcode = record.polling_station_postcode.strip()
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
            "internal_council_id": record.station_uprn.strip(),
            "postcode": record.polling_station_postcode.strip(),
            "address": self.get_station_address(record),
            "location": location,
        }

    def address_record_to_dict(self, record):
        address = ", ".join(
            [
                record.electorate_address1.strip(),
                record.electorate_address2.strip(),
                record.electorate_address3.strip(),
                record.electorate_address4.strip(),
                record.electorate_address5.strip(),
                record.electorate_address6.strip(),
            ]
        )
        while ", , " in address:
            address = address.replace(", , ", ", ")
        if address[-2:] == ", ":
            address = address[:-2]

        return {
            "address": address.strip(),
            "postcode": record.electorate_postcode.strip(),
            "polling_station_id": record.station_uprn.strip(),
        }
