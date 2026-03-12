from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = (
        "2026-05-07/2026-03-12T15:58:21.255699/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-12T15:58:21.255699/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023121146",  # 210A TOPSHAM ROAD, EXETER
            "10091473295",  # EXE VIEW LODGE, STOKE HILL, EXETER
        ]:
            return None

        if record.addressline6 in [
            # split
            "EX4 5AJ",
            "EX2 7TF",
            "EX2 7AY",
            "EX4 9HE",
            # looks wrong
            "EX3 0GF",
        ]:
            return None
        return super().address_record_to_dict(record)
