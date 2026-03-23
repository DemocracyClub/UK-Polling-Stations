from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRW"
    addresses_name = (
        "2026-05-07/2026-03-23T11:28:19.703638/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-23T11:28:19.703638/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "HA1 2LH",
            "HA5 3YJ",
            "HA5 3HF",
            # suspect
            "HA1 1HQ",
            "HA1 4GT",
        ]:
            return None
        return super().address_record_to_dict(record)
