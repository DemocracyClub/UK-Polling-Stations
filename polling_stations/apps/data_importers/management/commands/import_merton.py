from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MRT"
    addresses_name = "2024-05-02/2024-03-07T15:22:09.530001/Democracy Club Data.csv"
    stations_name = "2024-05-02/2024-03-07T15:22:09.530001/Democracy Club Data.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "KT3 6LZ",
            "CR4 2JR",
        ]:
            return None

        return super().address_record_to_dict(record)
