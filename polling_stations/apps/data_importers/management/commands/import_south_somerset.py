from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SSO"
    addresses_name = (
        "2022-05-05/2022-03-23T16:27:11.495824/polling_station_export-2022-03-23.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T16:27:11.495824/polling_station_export-2022-03-23.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "BA10 0BU",
            "BA22 8NT",
            "BA9 9NZ",
            "TA10 0DL",
            "TA10 0HF",
            "TA10 0PJ",
            "TA10 0QH",
            "TA11 7AU",
            "TA14 6TS",
            "TA20 2BE",
            "TA3 6RP",
            "TA10 9ER",
        ]:
            return None

        return super().address_record_to_dict(record)
