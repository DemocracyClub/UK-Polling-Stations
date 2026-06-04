from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = "2026-06-25/2026-06-04T11:23:46.503985/Democracy_Club__25June2026 - Updated (1).tsv"
    stations_name = "2026-06-25/2026-06-04T11:23:46.503985/Democracy_Club__25June2026 - Updated (1).tsv"
    elections = ["2026-06-25"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.post_code in [
            # split
            "WA10 1HT",
            "WA9 3RR",
        ]:
            return None
        return super().address_record_to_dict(record)
