from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOX"
    addresses_name = (
        "2026-05-07/2026-02-17T15:37:03.373996/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-17T15:37:03.373996/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "OX20 1RZ",
            # suspect
            "OX18 2BE",
            "OX18 4ET",
            "OX7 6BJ",
            "OX28 4HD",
            "OX18 3NU",
        ]:
            return None

        return super().address_record_to_dict(record)
