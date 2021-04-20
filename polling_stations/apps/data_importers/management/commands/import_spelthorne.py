from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SPE"
    addresses_name = "2021-04-01T14:28:58.464773/polling_station_export-2021-04-01.csv"
    stations_name = "2021-04-01T14:28:58.464773/polling_station_export-2021-04-01.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "TW18 1HE",
            "TW15 1AG",
            "TW15 3SH",
            "TW15 1QN",
            "TW16 7QQ",
        ]:
            return None

        return super().address_record_to_dict(record)
