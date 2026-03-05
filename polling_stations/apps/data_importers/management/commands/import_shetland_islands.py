from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ZET"
    addresses_name = "2026-05-07/2026-03-05T15:41:53.622621/Democracy Club - Idox_2026-03-05 11-54 (1).csv"
    stations_name = "2026-05-07/2026-03-05T15:41:53.622621/Democracy Club - Idox_2026-03-05 11-54 (1).csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "30100005132",  # BOOTH, OLLABERRY, SHETLAND
        ]:
            return None

        return super().address_record_to_dict(record)
