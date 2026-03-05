from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FAR"
    addresses_name = (
        "2026-05-07/2026-03-05T12:10:12.246938/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T12:10:12.246938/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "PO16 7LR",
            "PO14 3EU",
        ]:
            return None

        return super().address_record_to_dict(record)
