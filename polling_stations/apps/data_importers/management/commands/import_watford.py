from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "WAT"
    addresses_name = "2026-05-07/2026-02-16T14:24:39.850620/Democracy Club - Idox_2026-02-16 14-17.csv"
    stations_name = "2026-05-07/2026-02-16T14:24:39.850620/Democracy Club - Idox_2026-02-16 14-17.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # splits
            "WD25 7DA",
            "WD25 9AS",
            "WD18 7BS",
        ]:
            return None

        return super().address_record_to_dict(record)
