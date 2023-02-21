from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HMF"
    addresses_name = (
        "2022-05-05/2022-03-13T18:01:43.704952/polling_station_export-2022-03-13.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-13T18:01:43.704952/polling_station_export-2022-03-13.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "W14 9DS",
            "SW6 3QP",
            "W6 7RP",
            "SW6 7PT",
            "SW6 6BU",
            "W14 8UZ",
            "W6 0NQ",
        ]:
            return None

        return super().address_record_to_dict(record)
