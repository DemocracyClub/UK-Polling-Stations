from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CMN"
    addresses_name = (
        "2022-05-05/2022-03-03T09:57:57.949812/polling_station_export-2022-03-03.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-03T09:57:57.949812/polling_station_export-2022-03-03.csv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "SA33 5QQ",
            "SA14 9AW",
            "SA32 7AS",
            "SA34 0HX",
            "SA15 1HP",
            "SA16 0PP",
            "SA44 5YB",
            "SA32 8BX",
            "SA14 8TP",
            "SA16 0LE",
            "SA15 5LP",
            "SA31 3JJ",
            "SA14 8BZ",
            "SA14 8AY",
            "SA18 3TB",
            "SA18 2SU",
            "SA19 8TA",
            "SA34 0XA",
            "SA20 0EY",
            "SA19 8BR",
            "SA33 6HB",
            "SA19 7YE",
            "SA39 9HN",
            "SA14 8JA",
            "SA32 7QJ",
            "SA19 7SG",
            "SA39 9EJ",
            "SA17 5US",
            "SA17 4NF",
            "SA33 5DH",
            "SA18 3NB",
            "SA19 9AS",
            "SA19 7DL",
        ]:
            return None

        return super().address_record_to_dict(record)
