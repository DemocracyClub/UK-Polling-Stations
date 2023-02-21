from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MEN"
    addresses_name = (
        "2022-05-05/2022-04-21T09:56:14.599904/polling_station_export-2022-03-23-2.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-21T09:56:14.599904/polling_station_export-2022-03-23-2.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "BA11 4AJ",
            "BA3 5QE",
            "BA16 0NU",
            "BA11 2TQ",
            "BA16 0BD",
            "BA11 4SA",
            "BA5 1RJ",
            "BA11 5BT",
            "BA5 3QR",
            "BA11 5EP",
            "BA6 9DH",
            "BA16 0JL",
            "BA11 2ED",
            "BA3 4DN",
            "BA16 0BG",
            "BA4 5HB",
            "BA11 2XG",
            "BA4 4DP",
            "BA4 4BT",
            "BA11 2AU",
            "BA11 4FJ",
            "BA11 4NY",
            "BA6 8AP",
            "BA11 5HA",
            "BA11 5DU",
        ]:
            return None

        return super().address_record_to_dict(record)
