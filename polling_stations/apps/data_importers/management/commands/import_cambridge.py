from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2025-05-01/2025-03-24T11:15:17.136445/Cab_fixed.csv"
    stations_name = "2025-05-01/2025-03-24T11:15:17.136445/Cab_fixed.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CB4 1LD",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
