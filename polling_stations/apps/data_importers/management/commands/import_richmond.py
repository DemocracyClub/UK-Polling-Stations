from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIC"
    addresses_name = (
        "2026-05-07/2026-03-30T12:14:37.213686/Democracy_Club__07May2026 (1).CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-30T12:14:37.213686/Democracy_Club__07May2026 (1).CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if (
            uprn
            in [
                # "10094588154",  # 42 ROSSLYN AVENUE, LONDON
            ]
        ):
            return None
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "TW2 5NJ",
            "TW12 2SB",
        ]:
            return None
        return super().address_record_to_dict(record)
