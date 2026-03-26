from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STY"
    addresses_name = (
        "2026-05-07/2026-03-11T10:30:53.150481/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-11T10:30:53.150481/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "103001354",  # MANAGERS ACCOMMODATION THE STORYBOOK ABINGDON WAY, SOUTH TYNESIDE, BOLDON COLLIERY
                "200000006403",  # THE COTTAGE, WHITBURN MOORS FARM, SUNDERLAND ROAD, SUNDERLAND
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "NE31 2EA",
            "NE34 8AE",
            "NE34 7QZ",
            # looks wrong
            "NE32 3EA",
            "NE31 2HP",
            "NE32 5QF",
            "NE32 3EA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # station postcode fix + coords from council for:
        # Portable Station, Monkton Lane On grassed area near path leading to Hexham Ave Jarrow NE31 2DG
        if record.polling_place_id == "6221":
            record = record._replace(
                polling_place_postcode="NE31 2GD",
                polling_place_easting="431496",
                polling_place_northing="562936",
            )
        return super().station_record_to_dict(record)
