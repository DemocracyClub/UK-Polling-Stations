from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HUN"
    addresses_name = (
        "2025-05-01/2025-03-10T17:31:30.888147/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T17:31:30.888147/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "PE19 1HW",
            "PE28 2QG",
        ]:
            return None

        return super().address_record_to_dict(record)
