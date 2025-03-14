from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOC"
    addresses_name = (
        "2025-05-01/2025-03-14T11:42:13.125033/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-14T11:42:13.125033/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090440987",  # FLAT AT THE BEDWARDINE 128 BROMYARD ROAD, WORCESTER
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Location correction for: Henry Sandon Hall Royal Porcelain Works, WR1 2NE
        if record.polling_place_id == "7018":
            record = record._replace(
                polling_place_easting="385149",
                polling_place_northing="254311",
            )

        return super().station_record_to_dict(record)
