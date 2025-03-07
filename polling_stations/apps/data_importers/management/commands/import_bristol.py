from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BST"
    addresses_name = (
        "2025-05-01/2025-03-07T11:57:12.448976/Democracy_Club__01May2025_2025-03-07.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-07T11:57:12.448976/Democracy_Club__01May2025_2025-03-07.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "310372",  # THE BUNGALOW, GOLF COURSE LANE, BRISTOL
        ]:
            return None

        if record.post_code in [
            # split
            "BS7 8JP",
            # suspect
            "BS14 0SW",
        ]:
            return None
        return super().address_record_to_dict(record)
