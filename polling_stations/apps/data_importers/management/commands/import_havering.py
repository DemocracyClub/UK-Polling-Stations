from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAV"
    addresses_name = (
        "2026-05-07/2026-02-09T12:13:49.257559/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-09T12:13:49.257559/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021384326",  # 97 LOWER BEDFORDS ROAD, ROMFORD
            "10033422378",  # 17 KILN WOOD LANE, HAVERING-ATTE-BOWER, ROMFORD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RM7 8DX",
            "RM12 4LG",
            "RM7 7BX",
            "RM11 2BY",
        ]:
            return None

        return super().address_record_to_dict(record)
