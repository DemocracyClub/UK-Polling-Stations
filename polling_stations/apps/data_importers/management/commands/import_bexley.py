from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BEX"
    addresses_name = (
        "2026-05-07/2026-04-07T10:21:58.209697/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-07T10:21:58.209697/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094789367",  # 51A MAYPLACE ROAD WEST, BEXLEYHEATH
            "10094790360",  # 1 FEN GROVE, SIDCUP
            "100020267460",  # 69 CUMBERLAND AVENUE, WELLING
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "DA14 6NE",  # LAWRENCE COURT, SIDCUP
        ]:
            return None
        return super().address_record_to_dict(record)
