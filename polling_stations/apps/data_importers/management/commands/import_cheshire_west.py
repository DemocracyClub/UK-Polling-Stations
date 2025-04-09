from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHW"
    addresses_name = (
        "2025-05-01/2025-04-09T10:19:06.202417/Democracy_Club__01May2025 (12).tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-09T10:19:06.202417/Democracy_Club__01May2025 (12).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "WA6 0JA",
        ]:
            return None

        return super().address_record_to_dict(record)
