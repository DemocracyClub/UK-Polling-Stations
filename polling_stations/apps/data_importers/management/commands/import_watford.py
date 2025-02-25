from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = "2025-05-01/2025-02-25T15:00:12.120364/Democracy Club Data.csv"
    stations_name = "2025-05-01/2025-02-25T15:00:12.120364/Democracy Club Data.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # splits
            "WD25 9AS",
            "WD18 7BS",
            "WD25 7DA",
        ]:
            return None

        return super().address_record_to_dict(record)
