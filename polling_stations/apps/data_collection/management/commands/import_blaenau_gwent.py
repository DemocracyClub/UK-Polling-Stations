from data_collection.base_importers import BaseStationsAddressesImporter


class Command(BaseStationsAddressesImporter):
    srid = 27700
    districts_srid = 27700
    stations_filetype = "shp"
    addresses_filetype = "shp"
    council_id = "W06000019"
    addresses_name = "parl.2017-06-08/Version 1/BGCBC Poll Districts.shp"
    stations_name = "parl.2017-06-08/Version 1/POLLSTATIONS.shp"
    elections = ["parl.2017-06-08"]

    def parse_string(self, text):
        try:
            return text.strip().decode("windows-1252")
        except AttributeError:
            return text.strip()

    def address_record_to_dict(self, record):
        record = record.record
        address_parts = [self.parse_string(x) for x in record[2:8]]
        address_parts = [x for x in address_parts if x]
        address = ", ".join(address_parts)
        return {
            "address": address,
            "postcode": self.parse_string(record[9]),
            "polling_station_id": self.parse_string(record[1]),
        }

    def station_record_to_dict(self, record):
        stations = []
        codes = self.parse_string(record[1]).split("/")
        for code in codes:
            code = code.strip()
            stations.append(
                {
                    "internal_council_id": code,
                    "postcode": self.parse_string(record[6]),
                    "address": "\n".join(
                        [self.parse_string(record[4]), self.parse_string(record[5])]
                    ),
                }
            )
        return stations


"""
There are 1,562 properties which have a district code which does not correspond to a station.

The district codes are:
BD0001
BD0002
CF0001
CF0002
Q00001
Q00002
"""
