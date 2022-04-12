from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHO"
    addresses_name = (
        "2022-05-05/2022-03-28T09:45:04.518415/polling_station_export-2022-03-28.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-28T09:45:04.518415/polling_station_export-2022-03-28.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["PR7 2QL", "PR6 0HT", "PR6 0BS", "PR6 7YL"]:
            return None  # split

        return super().address_record_to_dict(record)
