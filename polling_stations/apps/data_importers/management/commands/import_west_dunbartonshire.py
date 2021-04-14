from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WDU"
    addresses_name = "2021-03-22T09:25:02.768761/polling_station_export-2021-03-21.csv"
    stations_name = "2021-03-22T09:25:02.768761/polling_station_export-2021-03-21.csv"
    elections = ["2021-05-06"]

    def get_stations(self):
        stations = super().get_stations()
        stations = [
            record for record in stations if record.streetname != "OTHER ELECTORS"
        ]
        return stations

    def get_addresses(self):
        addresses = super().get_stations()
        addresses = [
            record for record in addresses if record.streetname != "OTHER ELECTORS"
        ]
        return addresses

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "G81 3PY",
            "G81 5AW",
            "G81 5BL",
            "G60 5DP",
            "G82 3LE",
            "G82 3EY",
            "G82 4JS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.adminarea != "WEST DUNBARTONSHIRE":
            return None
        return super().station_record_to_dict(record)
