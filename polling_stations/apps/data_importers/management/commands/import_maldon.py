from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAL"
    addresses_name = "2026-05-07/2026-03-05T14:13:38.499642/Democracy_Club__07May2026 -2026.03.05.tsv"
    stations_name = "2026-05-07/2026-03-05T14:13:38.499642/Democracy_Club__07May2026 -2026.03.05.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094633716",  # PARK HOUSE MALDON ROAD, LATCHINGDON
        ]:
            return None

        if record.addressline6.strip() in [
            # split
            "CM9 4NY",
            "CM9 6YN",
            # suspect
            "CM9 4RA",
        ]:
            return None

        return super().address_record_to_dict(record)
