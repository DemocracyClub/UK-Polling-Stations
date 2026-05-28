from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABE"
    addresses_name = "2026-06-18/2026-05-28T12:59:29.293540/Aberdeen South_Democracy Club - Idox_2026-05-26 10-12 (1).csv"
    stations_name = "2026-06-18/2026-05-28T12:59:29.293540/Aberdeen South_Democracy Club - Idox_2026-05-26 10-12 (1).csv"
    elections = ["2026-06-18"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            "AB13 0HQ",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
