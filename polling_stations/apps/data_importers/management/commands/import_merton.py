from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MRT"
    addresses_name = (
        "2022-05-05/2022-04-07T16:25:02.632119/polling_station_export-2022-04-07.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-07T16:25:02.632119/polling_station_export-2022-04-07.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CR4 2JR",
            "KT3 6LZ",
            "SM4 6LF",
        ]:  # split
            return None

        return super().address_record_to_dict(record)
