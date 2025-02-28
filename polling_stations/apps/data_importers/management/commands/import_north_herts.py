from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NHE"
    addresses_name = (
        "2025-05-01/2025-02-28T15:19:33.716963/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-02-28T15:19:33.716963/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "SG8 8AD",
            # looks wrong
            "SG5 1ET",
        ]:
            return None

        return super().address_record_to_dict(record)
