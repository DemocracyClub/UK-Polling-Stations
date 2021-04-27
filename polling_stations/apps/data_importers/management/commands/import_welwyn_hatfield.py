from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WEW"
    addresses_name = "2021-04-16T15:42:48.310782/polling_station_export-2021-04-16.csv"
    stations_name = "2021-04-16T15:42:48.310782/polling_station_export-2021-04-16.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "AL10 0TA",
            "AL10 0SZ",
            "AL6 9AF",
            "AL6 9FJ",
            "AL6 9HT",
            "AL10 9BG",
            "AL7 2BQ",
        ]:
            return None

        return super().address_record_to_dict(record)
