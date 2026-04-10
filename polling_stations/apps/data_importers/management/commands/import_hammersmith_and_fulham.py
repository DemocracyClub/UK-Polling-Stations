from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "HMF"
    addresses_name = "2026-05-07/2026-04-10T10:10:51.457456/Democracy Club - Idox_2026-04-10 09-46.csv"
    stations_name = "2026-05-07/2026-04-10T10:10:51.457456/Democracy Club - Idox_2026-04-10 09-46.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()

        if uprn in [
            "34146774",  # THIRD FLOOR FLAT 95 HAMMERSMITH GROVE, LONDON
            "34003087",  # 4 STEVENTON ROAD, LONDON
            "34012656",  # 26 ALDENSLEY ROAD, LONDON
        ]:
            return None

        if record.postcode in [
            # splits
            "SW6 7JZ",
            "SW6 7PT",
        ]:
            return None

        return super().address_record_to_dict(record)
