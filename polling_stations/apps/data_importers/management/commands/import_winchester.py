from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = (
        "2025-05-01/2025-03-31T09:13:48.572996/Democracy_Club__01May2025 (7).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-31T09:13:48.572996/Democracy_Club__01May2025 (7).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "100062518967",  # 16 LIME CLOSE, COLDEN COMMON, WINCHESTER
            "100060605297",  # 18 LIME CLOSE, COLDEN COMMON, WINCHESTER
            "10090845084",  # FLAT 8, 4 ST, CROSS ROAD, WINCHESTER
        ]:
            return None
        return super().address_record_to_dict(record)
