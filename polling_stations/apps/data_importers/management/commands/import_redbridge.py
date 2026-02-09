from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDB"
    addresses_name = (
        "2026-05-07/2026-02-09T10:20:00.405023/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-09T10:20:00.405023/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10096145280",  # FLAT 5 65 CLEVELAND ROAD, ILFORD
        ]:
            return None

        if record.addressline6 in [
            # split
            "IG2 6FS",
            "IG2 6FR",
            "IG2 6FT",
            # looks wrong
            "IG6 1GS",
        ]:
            return None

        return super().address_record_to_dict(record)
