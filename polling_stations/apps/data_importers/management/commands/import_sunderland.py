from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2026-05-07/2026-04-10T12:25:39.636850/2026 10 04 Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-10T12:25:39.636850/2026 10 04 Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "45002135",  # SUNHILL, NORTH ROAD, HETTON-LE-HOLE, HOUGHTON LE SPRING
        ]:
            return None

        if record.addressline6 in [
            # split
            "SR2 9HN",
            "NE38 8PF",
            "DH4 4PG",
            "SR2 7AL",
            "SR2 7BQ",
            "SR3 3QH",
            # suspect
            "DH4 4FZ",
            "DH4 4FX",
            "DH4 4FW",
            "DH4 4FY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # fixing bad coords for: Sulgrave Centre Manor Road Sulgrave Washington
        if record.polling_place_id == "19902":
            record = record._replace(
                polling_place_easting="431374",
                polling_place_northing="558024",
            )

        # council coords correction for: Washington Village Hall, Valley Forge Washington, NE38 7JN
        if record.polling_place_id == "19970":
            record = record._replace(
                polling_place_easting="430880",
                polling_place_northing="556749",
            )

        return super().station_record_to_dict(record)
