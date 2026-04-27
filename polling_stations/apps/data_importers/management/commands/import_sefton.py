from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SFT"
    addresses_name = (
        "2026-05-07/2026-04-27T10:07:35.671275/Democracy_Club__07May2026 (2).tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-27T10:07:35.671275/Democracy_Club__07May2026 (2).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "41026136",  # 1 DOWNING ROAD, BOOTLE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L23 0SY",
            "L20 4JG",
            "L37 1PZ",
            "L30 7PD",
        ]:
            return None

        return super().address_record_to_dict(record)
