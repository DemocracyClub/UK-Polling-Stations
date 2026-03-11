from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HNS"
    addresses_name = (
        "2026-05-07/2026-03-11T15:52:07.464149/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-11T15:52:07.464149/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090801654",  # FLAT THE QUEENS HEAD 123 HIGH STREET, CRANFORD, HOUNSLOW
        ]:
            return None

        if record.addressline6.replace("\xa0", " ") in [
            # split
            "TW3 3DW",
            "W4 4EU",
            "W4 1TF",
            "TW4 5HS",
            "TW8 0QS",
            "TW13 6AB",
            "TW4 6DH",
        ]:
            return None

        return super().address_record_to_dict(record)
