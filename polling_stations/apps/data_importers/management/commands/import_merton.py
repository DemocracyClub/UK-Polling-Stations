from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MRT"
    addresses_name = (
        "2024-07-04/2024-06-01T11:42:53.841573/Democracy Club Data GE 2024.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-01T11:42:53.841573/Democracy Club Data GE 2024.csv"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "KT3 6LZ",
            "CR4 2JR",
        ]:
            return None

        return super().address_record_to_dict(record)
